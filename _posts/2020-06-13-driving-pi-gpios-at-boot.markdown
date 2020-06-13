---
layout: post
title:  "Controlling Raspberry Pi GPIOs at boot"
date:   2020-06-13 7:00 +0000
tags:   pi gpio boot
---

It is possible configure Raspberry Pi GPIOs very early on at boot time, by adding configuration to the /boot/config.txt file.  The detailed instructions are [here](https://www.raspberrypi.org/documentation/configuration/config-txt/gpio.md).

Here's an example - which with the [M-Bus Master Hat](https://www.packom.net/product/m-bus-master-hat/) powers up the M-Bus at boot time:

'''
gpio=26=op,dh
'''

Here:
* 26 is the pin number (using BCM pin numbering not wiringPi pin numbering)
* op means configure as an output
* dh means drive high (i.e. a 1)

This appears to override any configuration on the Hat's EEPROM, as the M-Bus Master Hat EEPROM configures the Pi to drive pin 26 low at boot - but with this configuration added to /boot/config.txt the pin goes high at boot and remains there.

