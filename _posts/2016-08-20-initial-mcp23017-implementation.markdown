---
layout: post
title:  "Initial MCP23017 implementation"
date:   2016-08-20 20:45:00 +0000
categories: mcp23017 gpio
---
# Initial MCP23017 implementation

[Second](/otb/otb-iot/pca9685/2016/08/19/initial-pca9685-implementation.html) on my list of I2C GPIO extenders to try out is the [MCP23107](https://www.microchip.com/wwwproducts/en/MCP23017).  This has 16 GPIOs in two banks of 8, supports interrupts, is available as a QFN package (as well as DIP and SSOP), but doesn't support PWM.

I have a basic working implementation of an MCP23017 driver in [otb-iot](https://github.com/piersfinlayson/otb-iot) although it's missing read support at the moment.  I'm finding that the device goes a bit squiffy if I read, so I'm probably doing something wrong.

Next up on my list of GPIO extenders to try is the [TI PCF8574](http://www.ti.com/lit/ds/symlink/pcf8574.pdf).  That has 8 GPIOs, and a very basic interface (just a single register with GPIO states.  (A 16 bit version is available.)  That's also available in a QFN package, hence my [QFN20 breakout board](/qfn20/vqfn/vqfn-20/qfn-20/oshpark/2016/08/19/qfn-20-breakout-board.html).  The PCF9574 is due on Monday - but the QFN20 is going to be somewhat longer so might be a while before I can try that out.

Once I have all three extenders up and running I'll do a comparison, including cost.
