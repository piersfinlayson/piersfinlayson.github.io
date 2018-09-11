---
layout: post
title:  "Differences between MCP23017 and MCP23018"
date:   2018-09-11 16:30:00 +0000
categories: i2c mcp23016 mcp23017 gpio
---

The [MCP23017](https://www.microchip.com/wwwproducts/en/MCP23017) is a very popular I2C 16 GPIO expander module, which you can use with various microcontrollers (e.g. Arduino, Raspberry Pi, ESP8266, ...) to extend the number of GPIOs at your command.

I've used the MCP23017 is various projects in the past, and while looking at options for a new project wondered about the [MCP23018](https://www.microchip.com/wwwproducts/en/MCP23018).  Sure, there's an [MCP23008](https://www.microchip.com/wwwproducts/en/MCP23008) which is an 8 GPIO variant, and [MCP23S17](https://www.microchip.com/wwwproducts/en/MCP23S17) which is an SPI 16 port variant.

But what's the MCP23018 and why isn't it as popular?

The key differences are that the MCP23018 adds:

* open drain outputs and higher total current sinking capability - 400mA vs 150mA across all ports

* higher top speed on the I2C interface - 3.4MHz vs 1.7MHz

* tolerance for voltages on input pins to 5.5V (irrespective of Vdd).

The MCP23018 has only 1 address pin, rather than the three on the MCP23017, but still allows up to 8 devices on the bus simultaneously - using voltage (via an external voltage source/divider).  I don't really understand the point of this given it doesn't use the freed up pins - perhaps to allow a 24pin QFN (vs 28 for the MCP23017 QFN).

Like the MCP23017 there's also an SPI variant of the MCP23018 (the MCP23S18), which has the same differences (except the SPI bus speed remains at 10MHz like the MCP23S17).

In terms of cost the MCP23018 is on RS's website at [£1.34](https://uk.rs-online.com/web/p/i-o-expanders/6696446/) each for a minimum order of 5, compared to [£1.066](https://uk.rs-online.com/web/p/i-o-expanders/0403816/) for the MCP23017.  (Ex-VAT prices.)

Finally, there is also an [MCP23016](https://www.microchip.com/wwwproducts/en/MCP23016), which is now not recommended for new designs.  This

* can sink up to 300mA

* requires an external resistor and capacitor to set the internal clock speed

* is neither pin compatible with the MCP23017 or MCP23018

* only supports up to 400KHz I2C.

Probably not one to be using.
 
