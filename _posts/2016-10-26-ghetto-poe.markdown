---
layout: post
title:  "Ghetto PoE"
date:   2016-10-26 16:30:00 +0000
categories: esp8266 poe ghetto usb
---

# Ghetto PoE

One of the main uses I have in mind for my esp8266 based modules is to monitor and control devices around the house.  I have run CAT6 cable within the walls to many locations, but not embedded power cables to the same locations.  I don't want to have to have trailing power leads to control the esp8266 devices, nor do I want to rely on battery power (the esp8266 is a power hungry chip).  Therefore I want to run power over the CAT6.

I could run proper 802.3af/at, and then step the 44V DC down to whatever I need.  However, this is expensive - PoE switches are quite pricey (and even 2nd hand ones hold their value well), and standalone PoE injectors come in at $10+.  And, 44V isn't much good for an esp8266, which requires 3.3V, so there's extra cost and bulky additional electronics required to step this down again.

I'm already building modules to power off 5V, using micro USB.  Therefore an obvious solution to run 5V directly over the CAT6 myself.  Now, there's some big downsides with this - voltage drop over long runs of CAT6 is likely to be an issue, and there's a limited amount of current CAT6 cable can carry.  However, I reckon I can carry 500mA of current at 5V fairly safely using all 4 pairs in the cable, and without a problematic power drop, over distances of up to about 10m.  I'll also need to be careful not to attach a 5V RJ45 to a real ethernet device!

So, I put together the first version of a "Ghetto" [(see definition 4)](https://www.urbandictionary.com/define.php?term=ghetto) PoE board which takes 5V off a micro USB connector and sends it out of an RJ45.  At the other end I'll tap off the cable directly.  In future - if this proves to be a viable approach - I might adapt my esp8266 boards to include an RJ45 to allow for easier termination.

<a target="_blank" href="https://oshpark.com/shared_projects/yyvMDXC1"><img src="/static/img/ghetto%20poe%205v%20v0.1%20front.png" alt="Ghetto PoE 5V v0.1 front"/></a>
<a target="_blank" href="https://oshpark.com/shared_projects/yyvMDXC1"><img src="/static/img/ghetto%20poe%205v%20v0.1%20back.png" alt="Ghetto PoE 5V v0.1 rear"/></a>

The BOM is pretty short:

* An RJ45 port, with LEDs (of which only the right, green, one is used to indicate power).  I've used the [Amphenol RJHS-4081](http://uk.rs-online.com/web/p/rj45-connectors/2578779/).

* Micro USB PCB mount connector.  I use cheapos from aliexpress.

* A current limiting 0603 resistor for the green LED to indicator when power is applied - I'm using a 1.5K to keep power usage down (2ma through the LED, which I've checked lights it).

* A 1206 0.5A hold current, 1A trip current resettable fuse.  I'm using [Littelfuse 1206L050YR](http://uk.rs-online.com/web/p/resettable-surface-mount-fuses/7874198/).

Pins 2/4/6/8 are +5V, pins 1/3/5/7 are ground.

Cost from [OSH Park](https://oshpark.com/) is $2.85 for 3 boards.  Probably another $1 for the parts for each board.