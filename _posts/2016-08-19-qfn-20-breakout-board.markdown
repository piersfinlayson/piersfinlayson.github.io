---
layout: post
title:  "QFN20 breakout board"
date:   2016-08-19 15:45:00 +0000
categories: qfn20 vqfn vqfn-20 qfn-20 oshpark
---
# QFN20 breakout board

In my search for I2C GPIO extension boards I've now ordered some [TI PCF8574](http://www.ti.com/lit/ds/symlink/pcf8574.pdf) chips.  These support 8 GPIO and 8 I2C addresses but no PWM.  As I'll potentially be wanting these for production use everntually - and because I want to buy the cheapest stuff available - I've gone for the VQFN20 package (PCF8574RGYR).  This is a 3.5 mm x 4.5 mm chip with 2 pins on 2 sides and 8 pins on the other two sides.

The prototype breakout board is available to order on [OSH Park](https://oshpark.com/) below:
<a href="https://oshpark.com/shared_projects/5WkdzDli"><img src="https://644db4de3505c40a0444-327723bce298e3ff5813fb42baeefbaa.ssl.cf1.rackcdn.com/80671101d585010d49945d9208b08ded.png" alt="PCB front"/></a>
<a href="https://oshpark.com/shared_projects/5WkdzDli"><img src="https://644db4de3505c40a0444-327723bce298e3ff5813fb42baeefbaa.ssl.cf1.rackcdn.com/72bab577f61782c9a231a84a3560973b.png" alt="PCB back"/></a>

As with the [QFN28](/pcb/otb/qfn/qfn28/2016/08/17/qfn-28-breakout-board.html) board, there's silkscreen areas front for the chip name, and on the rear for a serial number.

I managed to find a .bxl CAD drawing of the package on [TI's website](http://www.ti.com/product/PCF8574/quality), downloaded the free copy of [Ultra Librarian](http://www.accelerated-designs.com/ultra-librarian/), exported to an Eagle scr, and then imported into an Eagle library.  This saved me drawing it all myself in Eagle.

Looking at it now maybe I should have made it rectangular with 10 pins on each side.  But I like squares.

A snip at $2.60 for 3 of these.
