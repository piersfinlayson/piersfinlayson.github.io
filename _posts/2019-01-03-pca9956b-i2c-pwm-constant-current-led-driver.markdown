---
layout: post
title:  "PCA9956B 24 Channel I2C LED Driver"
date:   2019-01-03 18:28:00 +0000
categories: nxp pca9956b i2c pwm led driver
---

# Introduction

I mentioned in a [recent post]({% post_url 2018-09-22-htssop-38-pca9956b-breakout %}) that I was experimenting with the [PCA9956B](https://www.nxp.com/docs/en/data-sheet/PCA9956B.pdf) 24 channel I2C PWM Constant Current LED Driver, and had produced a breakout board for it:

<p/>
<a href="https://www.oshpark.com/shared_projects/ODML4jKn"><img src="https://644db4de3505c40a0444-327723bce298e3ff5813fb42baeefbaa.ssl.cf1.rackcdn.com/a8dc502bb65e3d419e10a5c8bfc1b472.png" alt="PCB front" width="100"/></a>
<a href="https://www.oshpark.com/shared_projects/ODML4jKn"><img src="https://644db4de3505c40a0444-327723bce298e3ff5813fb42baeefbaa.ssl.cf1.rackcdn.com/0886aa1eaeaddd4c1be385a02bb4d238.png" alt="PCB read" width="100"/></a>

I've now spent a bit of time using the IC, so wanted to capture some pertinent information about it here.

# PCA9956B Functional Overview

In some ways this IC can be viewed as an general purpose output expander than can be used by devices such as the Raspbery Pi, ESP8266, Arduino, etc.  There's quite a few of them about, including possibly the most popular
* [MCP23017]({% post_url 2016-08-20-initial-mcp23017-implementation %}) (and others in this family like the MCP23008, MCP23016, [MCP23018]({% post_url 2018-09-11-differences-between-mcp23017-and-mcp23018 %}) - and SPI variants MCP23S08, MCP23S17, MCP23S18)
* [PCF8574]({% post_url 2016-08-21-pcf8574-implementation %})
* [PCA9685]({% post_url 2016-08-19-initial-pca9685-implementation %})

The PCA9956B is a bit harder to get hold of than these other ICs (none on [aliexpress](https://www.aliexpress.com/wholesale?catId=0&initiative_id=SB_20190103101631&SearchText=pca9956b) as of writing!), and a bit more expensive.  However, it has some neat featues that the other ICs don't, including:

* PWM at 31.25kHz.  The PCA9685 supports variable PWM from 24-1526Hz, but I need something > 20kHz for a project I'm working on

* 24 ouput pins (vs 16 on the PCA9685 and 8-16 on the others)

* PWM duty cycle is configurable for each PIN (as it is on the PCA9685)

* Built in group dimming and blinking function

* Configurable on time offset for each pin (to allow current draw to be better balanced)

* 8-bit configurable current draw on each pin indendently.  Amongst other things this means each pin can be driven with a different voltage and no current limiting resistors are required (so long as you don't exceed the power dissipation capability of the IC)

* Entire 7-bit I2C address range supported

* Up to 3 configurable I2C sub addresses and an all call address to allow the device to be controlled as part of a group (also supported by the PCA9685)

* Error detection for each pin capable of detecting of detecting open and short circuit conditions

* IC over-temperature detection and automatic disablement

* I2C bus software reset instruction (also supported by the PCA9685)

The one big downside compared with the MCP devices and PC8574 is no input support, but that's not something I needed here (I can use one of the other devices when I need inputs).

# Electrical Characteristics

* Supports Vdd from 3-5.5V

* I2C input voltage from 0.7Vdd up to 5.5V

* Up to 65mA per pin

* 2.5A total current sink to ground

* 2.95W dissipation at 25C

* Up to 20V LED driver voltage

# Package

This IC is only available as a HTSSOP-38, so a bit more of a pain for prototyping than devices availabel as a PDIP.  Unless you order some prototype boards linked to above :-).

# Price

I just picked some up in quantities of 10+ from [Farnell](https://uk.farnell.com/) (Element 14) for £2.08 each (inc VAT).

This compares with ~£1.80 for the PCA9685 and ~£1.20 for the MCP23017.

# Software Control

As it's an I2C device it's pretty easy to program and control.  The only gotcha that initially hit me is that to turn on a LED from a device initialized to the default state you need to configure both current and PWM to non-zero values.

I couldn't immediately find any software packages out there for e.g. Arduino for controlling this IC - doesn't mean there aren't any, but it's not nearly as well supported as other devices.

I'm in the middle of building an HTTP microservice for controlling PCA9956Bs that'll run on any linux-based I2C bus master, and will publish that once it's mostly complete.

# Conclusion

"Neat device, would use again" - this will be my go to device for complex, high current, many pin I2C-based output control until I find something better!