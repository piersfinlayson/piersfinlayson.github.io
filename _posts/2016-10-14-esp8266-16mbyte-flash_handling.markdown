---
layout: post
title:  "ESP8266 16MB Flash Handling"
date:   2016-10-14 16:45:00 +0000
categories: esp8266 16MB flash eeprom
---

# ESP8266 16MB Flash Handling

In recent weeks a number of ESP8266 devices have become available offering more than the
previous defacto maximum of 4MB of flash memory.  Wemos's [D1 mini pro](https://www.wemos.cc/product/d1-mini-pro.html) offers 16MB of flash, and the ESP-100
claims to offer 8MB.

To put this in context, the original ESP8266 modules (such as the ESP-01) offered 512KB of flash, with the more recent ones (ESP-07) 1MB and then 4MB.  The maximum addressable flash memory of the ESP8266 is 16MB according to the datasheet.  (The ESP32 offers up to 4 x 16MB of flash.)

I don't have a particular need for > 4MB flash ([otb-iot](http://packom.net/otb-iot) currently only requires and supports 4MB) but my interest was tweaked in the larger flash chips, so I thought I'd give it a go.  I've experience of replacing flash chips from older modules to upgrade them from 1MB to 4MB, so figured 16MB would be the same.

# Butchering a D1 mini

From a hardware perspective I was right - this was simple.  I ripped the PCB EMI shield off a [Wemos D1 mini](https://www.wemos.cc/product/d1-mini.html) of which I have tons, took off the old flash chip with a cheapo hot air station, and replaced with a Winbond W25Q128FVSIG chip.  There's no great sources I could find for these in the UK, so got them off aliexpress, at £3.20 for 5 inc shipping.  They arrived quickly (couple of weeks).

The good thing about this particular flash chip variant is that it's the same package as the original so doesn't require any bending of pins to try and get it to fit - it's just a drop in replacement.  The 128 in the part number is the size - 128Mbits, 16MBytes.

# First tests

So, first thing to do was run a quick test with [esptool.py](https://github.com/themadinventor/esptool) and check that the right device ID was returned.

Here's the output from an original D1 mini (not the pro!):

```
$ esptool.py flash_id
Connecting...
Manufacturer: ef
Device: 4016
```

And here's the output from the modified D1 mini:

```
$ esptool.py flash_id
Connecting...
Manufacturer: ef
Device: 4018
```

To break this down:

* ef = Winbond

* Device is 2 hex bytes - so 0x4016 or 0x4018.  The low order byte actually indicates the size - so 0x16 or 0x18.

  * 0x16 = 22 decimal so the size is 2 ^ 22 = 4,194,304 = 4MB.

  * 0x18 = 24 decimal so the size is 2 ^ 24 = 16,777,216 = 16MB.

# Reading/writing to > 4MB flash

Things went a bit downhill at this point.  It turns out that most of the various tools to read/write to the flash over serial don't support reading/writing from > 4MB space.  Some fail obviously, some fail silently.

This led me on a merry investigation, during which I concluded the ESP8266 SPI flash functions don't natively support > 4MB flash.  This isn't just the SDK functions, but also as far as I can tell the ROM based access methods upon which the SDK (and other tools) rely.  This isn't quite the same as saying the chip doesn't support > 4MB flash (it does) but makes accessing this extra space trickier.

If you simply try and access data beyond 4MB on the flash from code running on the chip using one of the usual functions:

* spi_flash_erase_sector

* spi_flash_write

* spi_flash_read

it'll fail.

# On board access to > 4 MB flash

So, if the SDK and ROM SPI functions don't support > 4 MB flash, how can you do so from on board the device?

Upon booting the device, code that resides in the ROM creates an SpiFlashChip struct.  A pointer to this structure is placed at a well known location - 0x3fffc714.  The structure itself seems to always be placed at 0x3fffc718.  So within your ESP8266 code you can simply declare a variable to access this pointer as follows:

```
extern SpiFlashChip *flashchip
```

Your code will compile and link because the linker scripts declare "flashchip" as being located at 0x3fffc714.

You can then dereference this pointer from within your ESP8266 code to access the various data within the struct, which is structured as follows:

```
typedef struct{
        uint32  deviceId;
        uint32  chip_size;    // chip size in byte
        uint32  block_size;
        uint32  sector_size;
        uint32  page_size;
        uint32  status_mask;
} SpiFlashChip;
```

The most interesting stuff in this structure is:

* deviceId

* chip_size

I had expected devceId to show the manufacturer device information above - so 0x1640ef and 0x1840ef (due to the ESP's byte ordering) for 4MB and 16MB devices respectively.  However, in the 16MB flash case deviceId is populated with 0x1640ef not 0x1840ef.  Hmmm.  Looks like the ROM is actually reading the device ID but then setting the size byte as 0x16 isn't of 0x18!

Similarly, chip_size contains the size of the chip in bytes - but contains 4,194,304 in both the 4MB and 16MB cases.  Again, looks like the ROM has a max size of 4MB.

The way around this is to change the chip_size value to the actual value - 16,777,216 in the 16MB case.  Espressif have produced a [sample](http://bbs.espressif.com/viewtopic.php?f=7&t=2865) that recommends you wrap the usual SPI flash methods with code which changes the chip_size to the real figure immediately before an operation, and back again immediately afterwards.

Something like this:

```
uint32_t flash_size_sdk;     // Store off original figure here
uint32_t flash_size_actual;  // Store off correct figure here

SpiFlashOpResult _spi_flash_erase_sector(uint16 sector)
{
  int8 status=0;
  flashchip->chip_size = flash_size_actual;
  status = spi_flash_erase_sector(sector);
  flashchip->chip_size = flash_size_sdk; // restore chip size
  return status;
}

SpiFlashOpResult _spi_flash_write(uint32 des_addr, uint32 *src_addr, uint32 size)
{
  int8 status=0;
  flashchip->chip_size = flash_size_actual;
  status = spi_flash_write(des_addr, src_addr, size);
  flashchip->chip_size = flash_size_sdk; // restore chip size
  return status;
}

SpiFlashOpResult _spi_flash_read(uint32 src_addr, uint32 *des_addr, uint32 size)
{
  int8 status=0;
  flashchip->chip_size = flash_size_actual;
  status = spi_flash_read(src_addr, des_addr, size);
  flashchip->chip_size = flash_size_sdk; // restore chip size
  return status;
}
```

Your application should then call the replacement _spi_flash functions.  This works a treat.

I haven't tested what happens if you just change and leave the chip_size set to the higher value - it may well confuse other bits of the SDK/ROM if you do this.

# Sample test program

I've written a small SDK program which writes and then verifies that write to a sector at 1MB intervals on the flash chip, up to 16MB.  You can find the [sample program here](https://github.com/piersfinlayson/esp-sdk-samples/tree/master/eeprom), in amongst my other [SDK samples](https://github.com/piersfinlayson/esp-sdk-samples).

# Without using the SDK

So how to get this to work when not using the SDK?

(Why not use the SDK?  Well Richard Burton's excellent [rboot](https://github.com/raburton/rboot) is a very small bootloader for the ESP8266, which is designed to fit into a very small space on the flash and therefore needs to avoid including the SDK which contains lots of bloat.  I make use of this and figured it would be nice to be able to store application images above 4MB.)

If not using the SDK you're not using the spi_flash_* functions.  Instead you'll be using the ROM based SPIEraseSector, SPIWrite and SPIRead.

It turns out a similar trick works here too - just wrap the hardware routines with code that corrects and then replaces chip_size.  I have successfully accessed memory beyond 4MB from within a hacked version of rboot.

# Accessing > 4MB externally

What about reading/writing 4MB from an external tool (such as esptool, esptool.py, etc)?  Well, I'm still struggling with this.  I thought I'd had it working, but not as yet.  Some folks on Arduino and nodemcu boards claim to have achieved this so I'm still investigating.