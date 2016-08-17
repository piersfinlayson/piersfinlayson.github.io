---
layout: post
title:  "QFN28 breakout board"
date:   2016-08-17 16:00:00 +0000
categories: pcb otb qfn qfn28
---
# QFN28 breakout board

I'm doing some experimentation with otb-iot modules which can act as slaves to an otb-iot master - the master has WiFi in it and then communicates with a separate slave module via serial (such as I2C).  This theoretically reduces the costs of the breakout modules, fewer WiFi devices and IP addresses, and gives a, well, more modular design.  To be proven as a concept yet though.

One of the slave modules I'm experimenting with, and have a board on order for from [dirtypcbs](http://dirtypcbs.com) which uses an [MCP23017](https://cdn-shop.adafruit.com/datasheets/mcp23017.pdf) chip to act as I2C to GPIO module - giving me 16 GPIOs from one I2C slave.  I'm going to use it drive relays initially, but could use it for a lot more.

Due to space constraints on the PCB I decided to go with the smallest package I could, with is a [QFN28](https://en.wikipedia.org/wiki/Quad_Flat_No-leads_package) - a 6mm x 6mm chip with 28 pins, all underneath the package (similar to the ESP8266 in fact).

As the MCP23017 as a QFN isn't any cheaper from China than in the UK, it means I already have the MCP23017s, but no way to use them.  My own PCBs aren't good enough quality to go down to 0.65mm pin pitch (my laser printer just isn't high res enough), and I don't want to solder leads onto the pads.  Couldn't find any off the shelf breakout boards ([QFN32](https://www.adafruit.com/product/1163) is reasonably available) so, I've designed my own QFN28 breakout board and have it on order from [OSH Park](https://oshpark.com), costing $4.25 for 3.  Hopefully these'll arrive a little quicker than the dirtypcbs, but we'll see.

Here's the boards on OSH Park's website if you want to order your own.

<a href="https://oshpark.com/shared_projects/uRDjCiBm"><img src="https://644db4de3505c40a0444-327723bce298e3ff5813fb42baeefbaa.ssl.cf1.rackcdn.com/3bfd90958e882bb2b089f6239bffde23.png" alt="QFN28 PCB front"/></a>
<a href="https://oshpark.com/shared_projects/uRDjCiBm"><img src="https://644db4de3505c40a0444-327723bce298e3ff5813fb42baeefbaa.ssl.cf1.rackcdn.com/ed0a4c97dc1859b4bebd5f3bc17f1926.png" alt="QFN28 PCB rear"/></a>

You can see a big silkscreen box on the front - designed to write the ID of the chip on (to save your eyes trying to read it off the chip when you forget).  There's a smaller one of the rear, which I do on all my boards so I can add a serial number with a sharpie.  I've also added thermal vias on the QFN pad (missing from the Adafruit QFN32 breakouts) to dissipate heat.

Full disclosure - I also actually have some MCP23017s as a DIP, so I can be playing with these in the meantime :-).

Update: Actually, I've now found two QFN28 breakouts:

* [IC Breakout](http://www.icbreakout.com/products/breakout-boards/quad-flat-no-lead/qfn-28/), but that's for a 5mm x 5mm package with 0.5mm pitch, at $6.99 EACH.

* [Artekit](http://www.artekit.eu/products/breakout-boards/bbadapters/qfn-28-6x6mm-to-dip-adapter-pack-of-2/) who have the right product, at 2.90 Euros for 2 ... but an added 4 Euros for shipping.

OSH Park price of $4.25 for 3 includes shipping so is cheaper.  If I panelised and got from dirtypcbs they'd be $14 for 40.  I would probably get them quicker from Artekit though!
