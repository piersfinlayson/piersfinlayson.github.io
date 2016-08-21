---
layout: post
title:  "PCF8574 Implementation"
date:   2016-08-21 15:45:00 +0000
categories: pcf8574 gpio
---
# PCF8574 Implementation

Have now implemented, but [not tested](/mcp23017/gpio/2016/08/20/initial-mcp23017-implementation.html) support for the [PCF8574](www.ti.com/lit/ds/symlink/pcf8574.pdf) I2C GPIO extender.  This supports 8 IOs, and nothing else - no fancy config, no PWM - it's very bare bones.  However, it's very cheap - [RS](http://uk.rs-online.com/web/) are sending me 5 for about 50p each, plus VAT.  See [here](/qfn20/vqfn/vqfn-20/qfn-20/oshpark/2016/08/19/qfn-20-breakout-board.html) for the QFN20 breakout board required for prototyping.

