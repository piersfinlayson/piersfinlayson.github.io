---
layout: page
date:   2017-11-11 14:30:00 +0000
categories: code
permalink: "snow-led"
---

This Snowflake LED board is based around a PIC10F200 (202/204/206) microcontroller. 

<img src="/static/img/snow_led.JPG" alt="Snow LED board"/>

The code flashes LEDs connected to GPIO pins 0, 1 and 2, and changes the flashing pattern when GPIO 3 is pulled low and then released.

The assmebler code for the PIC is on github [here](https://github.com/piersfinlayson/pcb-code/blob/master/snow-led/pic.asm).

