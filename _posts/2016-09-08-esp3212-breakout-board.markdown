---
layout: post
title:  "ESP-3212 Breakout Board"
date:   2016-09-08 17:45:00 +0000
categories: esp32 esp-3212 breakout 
---
# ESP-3212 Breakout Board

The maker community is very excited about the production release of [Espressif's](https://espressif.com/) [ESP-32](https://espressif.com/en/products/hardware/esp32/overview).  This is the popular [ESP8266's](https://espressif.com/en/products/hardware/esp8266ex/overview) big brother - with added Bluetooth, a second core, tons more GPIOs, higher possible clock speed and hardware accelerated encryption all in a QFN48 (6mm x 6mm) package.

I'm not entirely sure whether I'm going to end up using the ESP-32 but it definitely looks like something I'd like to play with, so I ordered a few ESP-3212 modules from [aliexpress](http://www.aliexpress.com/item/ESP32-WiFi-Bluetooth-module-Dual-core-CPU-Ethernet-port-MCU-Low-power-Bluetooth-ESP-3212/32731347417.html?btsid=a991f468-aa7f-4583-94ab-fe1e22bfb2e8&ws_ab_test=searchweb201556_0%2Csearchweb201602_1_10057_10065_10056_10068_10037_10055_10054_10069_301_10059_10033_10058_10032_10073_10017_10071_10070_10060_10061_10052_10062_10053_10050_10051%2Csearchweb201603_1&spm=2114.01010208.3.1.lLuhCX) earlier.

As the ESP-3212 board isn't the most user friendly I'll be needing a breakout board.  I saw [one](https://oshpark.com/shared_projects/VzGRol8G) appear on [OSHpark](https://oshpark.com)'s [shared projects](https://espressif.com/sites/default/files/documentation/esp_wroom_32_datasheet_en.pdf) page yesterday, but it looked a bit inefficient to me - and $11.90 for 3 - and it seems to be for Espressif's own WROOM module.  So I designed a more compact version which is about half the price at $6.15 for three.

<a href="https://oshpark.com/shared_projects/GdioABZ9"><img src="https://644db4de3505c40a0444-327723bce298e3ff5813fb42baeefbaa.ssl.cf1.rackcdn.com/7331a9310d73024be6a9a3b40cc30075.png" alt="ESP-3212 PCB front"/></a>
<a href="https://oshpark.com/shared_projects/GdioABZ9"><img src="https://644db4de3505c40a0444-327723bce298e3ff5813fb42baeefbaa.ssl.cf1.rackcdn.com/4493008197a0bcf6610c986b9a7043e5.png" alt="ESP-3212 PCB front"/></a>
 
Key differences with my board:

* Mine's designed for the ESP-3212, not the ESP32-WROOM from Espressif.

* Kept the antenna within the curtilage of the breakout board - to keep it tidy and reduce the total footprint of the completed item.  There's no ground plane so this shouldn't affect performance of the attenna (and I've done dreadful things to these PCB trace attennae before with very few ill effects!).

* Broke out the bottom pins perpendicular to the others.  This makes it less suitable for use in a breadboard, but I tend not to use these anyway.

* Didn't bother numbering the pins (don't think it's really necessary).

Of course, as I don't have any ESP-3212 boards yet I haven't tested, so order and use at your own risk!  I'm a bit nervous that the Eagle library I used has a 1.5mm pin pitch, and I've not seen any specs for the ESP-3212 yet.  But if it doesn't work I've only lost 6 bucks!

I've open-sourced the Eagle .brd and .sch files for this design under the GPLv3 [here](https://github.com/piersfinlayson/open-source-pcb-designs), and am grateful to [MacroYau](https://github.com/MacroYau) for their [Eagle library](https://github.com/MacroYau/MacroYau-Eagle-Libraries).
