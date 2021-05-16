---
layout: post
title:  "Booting from the 16th Megabyte of Flash on the ESP8266"
date:   2016-10-16 19:45:00 +0000
categories: esp8266 rboot bootloader
---

# Booting from the 16th Megabyte of Flash on the ESP8266

Finally managed to persuade an ESP8266 to boot from an image stored beyond the first 4MB of flash.

I'm using [Rboot](https://github.com/raburton/rboot) as my bootloader (I would strongly suspect booting from an image beyond 4MBs just isn't possible with the Espressif one).

Richard has [documented in some detail](http://richard.burtons.org/2015/06/11/memory-map-limitation-workaround/) the lengths you have to go to to boot from images beyond _1MB_ on the flash chip, which all stem from the fact that the ESP8266 can only map a 1MB window (aligned on a 1MB boundary) into the address space at once.

However, as rboot's "big flash" support theoretically already supports up to 16MB flash (the maximum the ESP8266 supports), I hoped it would be easy to get it to boot from beyond 4MB.

It may have been quicker for someone else, but it took me quite some time to realise the trick.  I've talked in a [previous post](/esp8266/16mb/flash/eeprom/2016/10/14/esp8266-16mbyte-flash_handling.html) about needing to modify a data structure used by the built in ESP8266 SPI flash functions to persuade the chip to access beyond 4MB of data.

It turns out to persuade ESP to boot from beyond 4MB of data ... you need to set flashchip->chip_size to 16,777,216 (or at least a large enough number to encompass your entire image) before jumping to the load address in your application image.

Well, of course you do - otherwise the device isn't going to be able to load and execute your code, as it thinks it's beyond the maximum size of the flash device.  before realising this I got various exceptions in the ROM memcpy and memcmp functions.

Just stick the following code before the return in check_image() in rboot.c:

~~~~~~
flashchip->chip_size = 16 * 1024 * 1024;
~~~~~~

