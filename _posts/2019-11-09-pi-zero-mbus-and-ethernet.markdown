---
layout: post
title:  "Running M-Bus Master and Ethernet Hats on a Pi Zero simultaneously"
date:   2019-10-15 8:52 +0000
tags:   pi zero mbus m-bus power energy ethernet hat
---

After [a comment](http://disq.us/p/256sd7z) on my article about [what's wrong with the Pi Zero](https://piers.rocks/2019/10/15/whats-wrong-with-the-pi-zero.html) suggested it's to do with the lack of fixed network connectivity on the Zero, I bought a [Waveshare Ethernet/USB Hub Hat](https://www.waveshare.com/eth-usb-hub-hat.htm) for the Pi Zero and tested it with the [M-Bus Master Hat](https://www.packom.net/m-bus-master-hat/).  The tl;dr is that they interoperate just fine.

Some observations about the Waveshare Hat:

* It's not a "Hat" according to the [Raspberry Pi Hat specifications](https://github.com/raspberrypi/hats) primarily because it doesn't include an EEPROM to allow the Pi to detect whether and what sort of a Hat is connected.  This is actually a good thing for interop with other Hats, as the spec doesn't support mulitple Hats (and therefore EEPROMs) simultaneously.  This means with both Hats connected the Pi can detect the M-Bus Master Hat.

* The Ethernet Hat only appears to use the GPIO connector for power, passing all GPIOs (and other pins) through.  Therefore GPIO 26, which the M-Bus Master Hat uses to control M-Bus power, works fine, as do the serial pins which the M-Bus Master Hat uses to communicate with slave devices.

* The [Realtek RTL8152B 10/100M](https://www.realtek.com/en/products/communications-network-ics/item/rtl8152b-n) Ethernet driver IC is used by the Ethernet Hat.  This is supported by the Raspbian kernel out of the box, meaning plug and play.

* There is a [schematic](https://www.waveshare.com/w/upload/0/08/ETH_USB_HUB_HAT.pdf) available for the Ethernet Hat (just as this is for the [M-Bus Master Hat](https://www.packom.net/wp-content/uploads/2019/10/M-Bus-Master-Hat-schematic-v1.4.pdf)).  This is handy to see how the Ethernet (and USB hub function) on the Waveshare Hat works, and for integrating into your own designs.

* There is a small physical issue with running both Hats at the same time - the ethernet port on the Waveshare Hat ends up directly under an opto-isolator on the M-Bus Master Hat, meaning the M-Bus Hat doesn't sit fully home on the Waveshare GPIO pin header, but works fine not seated fully home.  I'd recommend using a 12mm spacer between the Hats.

* As the Ethernet Hat uses USB rather than GPIOs to provide the ethernet connectivity it comes with a funky double micro-USB male board, which connects the second micro-USB port from the Pi Zero to the Ethernet Hat.  This works well as a solution, and provides additional rigidity to the Ethernet Hat even if not using spacers.  2 spacers do come with the Hat, which is a bit stingy when they cost at most a few pennies.  I assume they are intended to be used on the side of the board without the GPIO connector.

All in all this Hat seems like a decent solution for providing fixed ethernet connectivity to a Zero and connecting other Hats at the same time.