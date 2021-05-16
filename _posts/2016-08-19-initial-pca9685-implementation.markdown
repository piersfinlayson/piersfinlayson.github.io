---
layout: post
title:  "Initial PCA9685 Implementation"
date:   2016-08-19 19:45:00 +0000
categories: otb otb-iot pca9685
---
# PCA9685 Implementation

Following on from my [rant](/rant/hobbyists/libraries/2016/08/18/rant-about-hobbyist-software.html) about hobbyist software libraries I have now written an initial implementation of a [PCA9685](http://www.nxp.com/products/power-management/lighting-driver-and-controller-ics/i2c-led-display-control/16-channel-12-bit-pwm-fm-plus-ic-bus-led-controller:PCA9685) driver from scratch.  And you know what?  It detects failures and reports them so it's easier to figure out when and where something is failing!

It's available in the [otb-iot](https://github.com/piersfinlayson/otb-iot) codebase.

Pretty basic right now - just flashes LED 0 connected to device at address 0x40 on and off every second.

