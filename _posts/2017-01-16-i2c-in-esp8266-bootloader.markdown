---
layout: post
title:  "I2C Within ESP8266 Bootloader"
date:   2017-01-16 15:30:00 +0000
categories: esp8266 i2c rboot
---

# Why?

Mostly because it seemed like an interesting idea.

For otb-iot I want to encode various information permanently on the device.  The flash associated with the ESP8266 isn't a good choice for this because the data there is considered pretty transient.  For example:

* The bootloader I'm using ([rboot](https://github.com/raburton/rboot)) will look for boot config when it first starts, and if it isn't present will write it - and also update this information with the slot to boot from as OTA updates happen.

* OTA updates happen, which causes entire new firmware images to be written to locations on the flash.

* The otb-iot software has its own config store on the flash device, which is updates as the user configures services (such as what relays to turn on upon boot, what I2C ADC device is attached at what address, and so on).

* [Modifications](http://www.packom.org/esp8266/rboot/bootloader/2016/10/15/using-rboot-for-the-esp8266.html) I've made to rboot allow it to take a factory flashed firmware and overwrite boot slot 0 with this for disaster recovery.

* The ESP8266 SDK also updates its own areas of the flash with information about rf calibration, AP credentials, etc.

The solution I've gone for is an [I2C eeprom](http://www.packom.org/esp8266/mcp/24aa00/i2c/2016/10/01/mcp-24aa00-family.html), specifically the [MCP 24LC128](https://www.microchip.com/wwwproducts/en/24LC128).  This is a 128kbit (16kB) eeprom, which can be progammed and read via I2C.  It also has write protect support, so I can write details to the eeprom and then write-protect the contents so it is more difficult to wipe or change them later.

As I played around with the eeprom it occured to me that it would be useful to be able to access it from within the bootloader - so the bootloader can check details written at the factory (and therefore trusworthy) and make decisions based on that.  Such as whether there's a status LED, and which GPIO it's connected to, so the bootloader can control that LED (e.g. to signal failed boot).

(Of course, I need to handle failures to read or parse the information without device being bricked - you want a bootloader to be pretty good about actually booting the device!)

As I'm also producing otb-iot boards with different ESP module types, ADCs, etc, there's some value in being able to detect this info, both from the bootloader and the otb-iot firmware itself.

# How?

I like pasko-zh's [brzo_i2c](https://github.com/pasko-zh/brzo_i2c).  It's small, fast, handles errors gracefully, and it works.  So I built this into otb-iot's version of [rboot](https://github.com/piersfinlayson/otb-iot/tree/master/lib/rboot), along with my [24lc128 reading code](https://github.com/piersfinlayson/otb-iot/blob/master/src/otb_i2c_24xxyy.c).

The issues I hit were pretty straightforward to resolve:

* The first problem is that rboot.bin was previously coming in at under 4096 bytes (or one flash sector).  As I had rboot located at 0x0, the boot config at 0x1000 and then firmware images at 0x2000 (and 0x202000) I needed to shift everything after rboot out.  Even though rboot has only ended up at just beyond 8192 bytes I've now set aside 24KB for rboot, and 8KB for config (where it was previously 4KB for each).

  There's a few places you need to touch to achieve this:

  * rboot itself - as rboot needs to know where the firmware images it's going to boot are.  (I [share](https://github.com/piersfinlayson/otb-iot/blob/master/include/otb_flash.h) a flash map between otb-iot and rboot so changing in one place affects both builds - although in reality the otb-iot firmware doesn't care where it lives - but the same map points to useful stuff like otb-iot's config location.)  
  
  * The otb-iot [linker script](https://github.com/piersfinlayson/otb-iot/blob/master/ld/eagle.app.v6.ld) - which again needs to know where within the 1MB window (aligned with a 1MB boundary) the ESP8266 has paged in the image will be. See the irom0_0_seg - address should be 0x40200010 + offset from 1MB of your image (so + 0x8000 in my case, made up of 24KB for boot and 8KB for the boot config).
  
  If you get this wrong the impact will be the chip cyclically throwing exceptions once rboot attempts to load the image.
  
* Second the brzo_i2c source sticks ICACHE_FLASH_ATTR in front of the _setup() routine, so it's stored on flash and only loaded into RAM by the SDK when the function is run.  There is no SDK here to load into RAM, so again, if rboot calls _setup() here you'll get cyclic exceptions.  The solution is to remove the ICACHE_FLASH_ATTR (or undefine it as I've done, when compiled alongside rboot).  Note the actual I2C read/write routines are already missing the ICACHE_FLASH_ATTR - to ensure high, reliable performance of brzo_i2c.

* The trickiest to solve was the fact that brzo_i2c (and my 24lc128 reading code) uses some global variables.  These are initialized either by implication (the C standard insists that globals are initialized to zero unless otherwise initialized) or explicitly in the C code.  This initialization happens either in the bss or data sections of the compiled executable.  The platform is then responsible for loading these sections to initialize the globals.

  However, the version of rboot I picked up used esptool2 (also from raburton) to create the .bin and omitted the bss and data sections.  Therefore the globals - such as i2c_error - never got initialized.  I had to modify my Makefile to include the bss and data sections and this problem went away.  I think the reason for omitting data and bss was to reduce the size of the bootloader binary as much as possible.  But as I'm only at around 9KB right now it's not a big deal.
  
  This took a long time to figure out, but I learnt a lot more about linker scripts, compilers and the C standard while I was at it :-).

# What?

Here's output from otb-iot's new I2C enabled bootloader reading factory encoded data from the 24LC128 eeprom - the new stuff is prefixed "EEPROM":

    BOOT: OTA-BOOT v0.2
    BOOT: OTA-Boot based on rBoot v1.2.1 - https://github.com/raburton/rboot
    BOOT: Checking GPIO14 o
    EEPROM: Eeprom size:            16384 bytes
    EEPROM: Global info format:     V1
    EEPROM: Global checksum:        0xe33d5406
    EEPROM: Global checksum:        Valid
    EEPROM: Hardware info format:   V1
    EEPROM: Hardware checksum:      0xd4585ca6
    EEPROM: Hardware checksum:      Valid
    EEPROM: Device serial:                    10002
    EEPROM: Hardware code/sub code: 00000001:00000001
    EEPROM: Chip ID:                c30418
    EEPROM: MAC 1:                  5c:cf:7f:c3:04:18
    EEPROM: MAC 2:                  5e:cf:7f:c3:04:18
    EEPROM: ESP module type:        1
    EEPROM: Flash Size:             4194304 bytes
    EEPROM: ADC Type(s):            0
    EEPROM: ADC Config(s):          0
    EEPROM: Internal SDA pin:       -1
    EEPROM: Internal SCL pin:       -1
    EEPROM: External SDA pin:       4
    EEPROM: External SCL pin:       5
    BOOT: Flash Size:   32 Mbit
    BOOT: Flash Mode:   QIO
    BOOT: Flash Speed:  40 MHz
    BOOT: Option: Big (>1MB) flash
    BOOT: Option: Config checksum
    BOOT: Option: IROM checksum
    BOOT: Booting rom 0 at 0x00050080
    BOOT: mmap 0,0,1
    rf[112] : 03
    rf[113] : 00
    rf[114] : 01

# Writing the Eeprom

I'm writing the eeprom data using a raspberry pi zero, along with

* a tool, [hwinfo](https://github.com/piersfinlayson/otb-iot/tree/master/tools/hwinfo), I've written to encode the data to be written to binary files

* eeprog, which takes the binary files and actually does the eeprom writing

* a little jig I use to connect the pi to my otb-iot board, which also allows the write-protect function on the eeprom to be temporarily turned off to allow writing.

The hwinfo tool uses the same [header](https://github.com/piersfinlayson/otb-iot/blob/master/include/otb_eeprom.h) to encode the eeprom data as otb-iot (and rboot) use to decode the information to ensure there are no inconsistencies in formatting.

I found [this article](http://www.richud.com/wiki/Rasberry_Pi_I2C_EEPROM_Program) really useful for getting I2C working on the pi.  Note however, that it omits the need to "modprobe i2c-dev" after rebooting the pi to enable the I2C bus...