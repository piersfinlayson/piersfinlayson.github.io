---
layout: post
title:  "Rboot mods for the ESP8266"
date:   2016-10-15 14:45:00 +0000
categories: esp8266 rboot bootloader
---

# Rboot mods for the ESP8266

[Rboot](https://github.com/raburton/rboot) is an open-source bootloader for the ESP8266.  Richard Burton, who wrote it, lists the reasons for its superiority over the one supplied in the ESP8266's SDK from Espressif in his [blog](http://richard.burtons.org/2015/05/18/rboot-a-new-boot-loader-for-esp8266/), but I'd summarise them as rboot providing the ultimate in flexibility.

As it's open source you're able to go in modify and add features to your heart's content, and it's simple enough to actually get your head around.  

I've used rboot with some customizations in my [Out of the Box Internet of Things (otb-iot)](/otb-iot/) firmware because I can use it to help make a much more reliable and robust Thing for the Internet - otb-iot's whole raison d'être!

In this post I'll run through all of my mods to rboot.

# ROM Validation

I use [esptool2](https://github.com/raburton/esptool2) (also by Richard Burton) to create otb-iot application images.  This allows me to stamp the image with a checksum when building it, which rboot can then use to validate the integrity of the application image on flash before booting. 

# Dual application images

I've decided to have two application images within my device, one of which will be the primary (active, booted) application, with the other available both as

* a slot to install a new image (so I can support Over the Air, OTA, updates)

* a backup in case the current active image gets corrupted, and can't be loaded.

As of the time of writing I've gone for the following addresses on my flash device (where otb-iot currently supports 4MB flash) for these two images:

* Slot 0 - 0x002000 

* Slot 1 - 0x202000

The reason for slot 0 being at 0x2000 is that

* rboot lives at 0x0

* rboot configuration lives at 0x1000

(These addresses may be about to change - I'm working on a new mod for rboot which causes it to grow beyond 4096 bytes, meaning I need to push the config out to 0x2000, and slot 0 to 0x3000.)

Slot 1 lives at 0x202000 as

* I use the megabyte at 0x100000 to store various logging and problem reporting information.

* I wanted to keep the 8192 byte offset for symmetry with slot 0.

It should be obvious by this stage that I've enable the big flash support within rboot to handle flash of greater than 1MB in size.  (Note however that it doesn't yet support >4MB flash.)

As well as the ability to switch between slots from the bootloader, and when upgrading via  OTA updates, I've also provided the ability to query and change the boot slot via MQTT.

# Third fallback image

I wanted to gain further robustness and be able to deal with both application images being corrupted - for example if an upgrade write fails, and then the old image gets corrupted.  I experimented with a few ways of doing this, with my first idea being to allow a third "fallback" image to be booted (and potentially updated).

However, I concluded that 

* there was value in the third fallback image being only ever read (so the possibility of corruption was a low as possible)

* it'd also be nice to be able to reset the device to a "factory" software image (and config).

So, I've plumped for installing a factory software image at 0x302000 when I do an initial flash of the device.  (That 0x2000 offset's again for symmetry with the other images.)

You need to be a bit careful on a 4MB device not to use the _whole_ of the last megabyte of space, as the SDK writes various stuff late on - from 0x3fc000 onwards.  So with my approach I need to ensure my factory image is short enough to avoid being overwritten by the SDK.  (Right now I don't check or police this, but should probably do so in the Makefile.)

In the event that rboot fails to boot from either the current active slot, or the other one, it will copy the factory image over slot 0, and attempt to boot from that.  (It will not boot directly from the factory image.)

# Factory reset

What about if the bootloader itself fails to correctly handle the corruption of the images in both slots 0 and 1?  I added the ability to otb-iot to:

* be reset by GPIO14 being pulled low

* trigger a complete reset to factory defaults if held down for 15s during boot.

The first of these (resetting by pulling GPIO14 low) is implemented in the application image, but the latter needs to be in the bootloader.  So I've added some code to rboot to read the GPIO register on startup to see if GPIO14 is held low - and then if held low for 15s rboot

* writes the factory image over the one in slot 0

* resets the active slot to slot 0 (so the newly flashed factory image boots)

* clears all otb-iot config (which for reference is stored at 0x200000, but which is out of the scope of this post).

# Logging

I've added consistent logging to the otb-iot version of rboot - so the logs it produces over serial are the same as those produced by my application images.  This make debug output look neater.

(Sadly rboot logs appear at 74,880 baud on a regular ESP8266 module with 26MHz crystal, whereas I use 115,200 from my application code.  This is one reason I've started  developing my own ESP8266 [base module](/esp8266/2016/09/26/first-esp8266-module-design.html) with a 40MHz crystal (so output from the bootloader is also at 115,200).

<a href="https://oshpark.com/shared_projects/CB9dajcz"><img src="https://644db4de3505c40a0444-327723bce298e3ff5813fb42baeefbaa.ssl.cf1.rackcdn.com/dc7d989279a2e85cf2f7ce55a369ef9a.png" alt="otb-8266 v0.1 front"/></a>
<a href="https://oshpark.com/shared_projects/CB9dajcz"><img src="https://644db4de3505c40a0444-327723bce298e3ff5813fb42baeefbaa.ssl.cf1.rackcdn.com/bed313a1c614e799ecbeda190787617c.png" alt="otb-8266 v0.1 rear"/></a>

It should be possible to convince rboot to output serial at 115,200 baud, but I've not got around to doing this.  Also, if you flash your device at 115,200 the flash tool will normally just restart the board straight away at 115,200 irrespective of the crystal - so I figure 115,200 is a good all-round value to use.

# Boot delay

I've found it's desirable to add a two second delay before rboot actually does anything - to give me time to connect to the device over serial when resetting before the device does anything.

# Coding within the bootloader

It's slightly different working within the bootloader, mainly because you don't have access to the SDK functions.  Adding the SDK would mean massively increasing the size of the bootloader.

This means you have to be creative when adding code to rboot, to avoid using the SDK - and accept there's some stuff that'll be beyond you.  As a simple example - you don't use spi_flash_read (as this is an SDK function), you call SPIRead (which is a ROM function).  If you do find you need to use an SDK function, you'll need to figure out what it does (by disassembling) and then figure out to to reimplement in the bootloader.

Richard talks about this in his [blog](http://richard.burtons.org/2015/09/22/c-version-of-system_get_rst_info/).

# >4MB Flash

I'm working on support for >4MB flash sizes within rboot.  As detailed within my [recent post](/esp8266/16mb/flash/eeprom/2016/10/14/esp8266-16mbyte-flash_handling.html) this involves some extra code wrapping the SPIEraseSector, SPIRead and SPIWrite functions, and also finding an external tool which can also access this extra space.

While I do have rboot successfully accessing areas of the flash beyond 4MB I haven't yet been able to boot from these sections.  Right now my main problem seems to be that adding this extra function increases the size of rboot beyond 0x1000 bytes, and forces me to shift the offset of my images out, and then when booting the image the chip craps out.  Once I've got this working I'll be releasing a new version of otb-iot rboot capable of accessing >4MB flash sizes.

# Conclusion

It's been lots of fun working with rboot and getting involved with the ESP8266 at a lower level than the SDK.  Given the whole philosophy of otb-iot is to be a very reliable device, having the extra control rboot gives has been very useful.  I want to thank Richard Burton for producing great open source bootloader.  If anyone has any rboot questions give me a shout.

All of my [rboot code](https://github.com/piersfinlayson/otb-iot/tree/master/lib/rboot) is available on [github](https://github.com/piersfinlayson/otb-iot).
