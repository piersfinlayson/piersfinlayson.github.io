---
layout: post
title:  "A sample SC16IS752 program for the ESP8266"
date:   2018-01-14 16:30:00 +0000
categories: esp8266 sc16is752 i2c
---

# Why?

Despite the fact that the ESP8266 was designed as a serial-wifi device, I've recently found the need to extend the ESP's the UART support using an another IC, to allow myself to reliably interface to a heat meter supporting the M-Bus protocol.

* [otb-iot](http://www.packom.org/otb-iot/) uses the standard hardware serial port on GPIO 1/3 to output debug information.  I don't want to lose out on this debugging information, so don't want to use these PINs to connect to other devices.

* The ESP8266's hardware serial support can be remapped to pins 13 and 15.  Sadly I don't have pin 15 free in otb-iot - it's used for controlling the status LED (a WS2812B) - so I can't just temporarily remap the hardware UART to these pins.

* I've tried a [software serial library](https://github.com/plieningerweb/esp8266-software-uart) for the ESP8266 non-OS SDK and integrated this with the [otb-iot software](https://github.com/piersfinlayson/otb-iot) already, but sadly I'm finding it unreliable when communicating with a device at 2,400 baud.  I think this is because occasionally, because 2,400 baud takes so long to send data, the wifi is kicking in and delaying the RX interrupts, meaning I'm losing bytes.

# What?

My search for an external IC to solve this problem led me to NXP's [SC16IS752](https://www.nxp.com/docs/en/data-sheet/SC16IS752_SC16IS762.pdf), which provides a UART with I2C and SPI interface.  There's a few variants of this device:

* SC16IS740 - single UART, no GPIOs

* SC16IS750 - single UART, GPIOs

* SC16IS760 - single UART, GPIOs, faster SPI bus support

* SC16IS752 - dual UART, GPIOs

* SC16IS760 - dual UART, GPIOs, faster SPI bus support

I mostly chose the SC16IS752 as it's what [RS](https://uk.rs-online.com/web/) had in stock, for about £2.50 each - I don't need dual UART for my application, but the GPIOs are handy to provide status LEDs on a module based on the IC, without using up more ESP GPIOs.  The GPIOs don't have any fancy function like PWM, and may not be spare in some more advanced UART use cases (but they are in mine).

I built a [sample application](https://github.com/piersfinlayson/sc16is752-esp) to get to know the SC16IS752 IC.  This program:

* Uses the I2C interface

* Registers an interrupt handler to listen for interrupts from the device

* Soft resets the device

* Initialises the device at adress 0x48 (A0 and A1 pulled to VDD)

* Blinks GPIOs 0 and 1

* Sends "Hello World" at 2400,8,N,1

* Waits a while for received data - and if received outputs it to console

* Performs a hard reset of the device, by pulling the RESET pin low

* Outputs some stats

* Starts again

These are essentially the operations I intend to make use of in my finished device.

Hopefully the code will be useful to others getting to know the SC16IS devices.

# How?

Key wiring details to set this up yourself using an ESP based device (all pin numbers assume the SC16IS752 TSSOP-28):

* 1 RTSA - NC

* 2 CTSA - NC

* 3 TxA - Connect to Rx on receiving device - such as a USB-TTY on a windows PC, running putty connected to the appropriate COM port, with serial settings as above

* 4 RxA - Connect to Tx on receiving device - such as a USB-TTY on a windows PC, running putty connected to the appropriate COM port, with serial settings as above

* 5 Reset - Connect to ESP GPIO13, with 10K pull-up to 3.3V

* 6 Xtal1 - Connect to pin 1 of 1.8432MHz oscillator, with 10-22pF capacitor to Gnd

* 7 Xtal2 - Connect to pin 2 of 1.8432MHz oscillator, with 10-22pF capacitor to Gnd

* 8 Vdd - 3.3V

* 9 I2C - 3.3V

* 10 A0 - 3.3V

* 11 A1 - 3.3V

* 12 NC

* 13 SCL - Connect to ESP GPIO5, with 10K pull-up to 3.3V

* 14 SDA - Connect to ESP GPIO4, with 10K pull-up to 3.3V

* 15 IRQ - Connec to ESP GPIO12, with 1K pull-up to 3.3V (per datasheet)

* 16 CTSB - NC

* 17 RTSB - NC

* 18 GPIO0 - Connect to -ve leg of LED, with +ve connected to current limiting resistor (GPIOs are capable of 4mA per datasheet) then to 3.3V

* 19 GPIO1 - Connect to +ve leg of LED, with -ve connected to current limiting resistor (GPIOs are capable of 4mA per datasheet) then to 3.3V

* 20 GPIO2 - NC

* 21 GPIO3 - NC

* 22 Vss - Gnd

* 23 TxB - NC

* 24 RxB - NC

* 25 GPIO4 - NC

* 26 GPIO5 - NC

* 27 GPIO6 - NC

* 28 GPIO7 - NC

There wasn't anything too tricky once I've gone through the datasheet a few times - although table 33 - which indicates that the registers aren't actually as indicated in the rest of the document - is quite important to find.  (Essentially the device has duplicate sets of registers for UARTs A and B), and hence the registers listed elsewhere in the document are modified so duplicate sets can be addressed.)

# Output

Here's sample output from the program:

~~~~~~
Step 0 - init I2C bus
  I2C stack init ... success

Step 1 - soft reset device
  Reset SC16IS752 ...
  IOControl reg: 0x0e actual reg: 0x70 val: 0x08
  Read LSR register
  First read may fail:
    read failure: 2
  Second should succeed:
    success

Step 2 - initialize device
SC16IS752 init ...
  IER reg: 0x01 actual reg: 0x08 val: 0x01
  FCR reg: 0x02 actual reg: 0x10 val: 0x01
  LCR reg: 0x03 actual reg: 0x18 val: 0x03
  MCR reg: 0x04 actual reg: 0x20 val: 0x00
  IODir reg: 0x0a actual reg: 0x50 val: 0x03
  IOIntEna reg: 0x0c actual reg: 0x60 val: 0x00
  IOControl reg: 0x0e actual reg: 0x70 val: 0x00
  EFCR reg: 0x0f actual reg: 0x78 val: 0x00
  LCR reg: 0x03 actual reg: 0x18 val: 0x83
  DLL reg: 0x00 actual reg: 0x00 val: 0x30
  DLH reg: 0x01 actual reg: 0x08 val: 0x00
  LCR reg: 0x03 actual reg: 0x18 val: 0x03

Step 3 - turn GPIOs 0,1 on
  IOState reg: 0x0b actual reg: 0x58 val: 0xff

Step 4 - turn GPIOs 0,1 off
  IOState reg: 0x0b actual reg: 0x58 val: 0xfc

Step 5 - send "Hello World #1"
  Hello World #1

Step 6 - NOP

Step 7 - NOP

Step 8 - NOP

!!! Received data: h



!!! Received data: e



!!! Received data: l



!!! Received data: l



!!! Received data: o



Step 9 - NOP

!!! Received data:



!!! Received data: b



!!! Received data: a



!!! Received data: c



Step 10 - NOP

!!! Received data: k



!!! Received data:



Step 11 - NOP

Step 12 - NOP

Step 13 - NOP

Step 14 - hard reset device
  Resetting device ... done
  Checking device reset ... success

Step 15 - Output stats
  Cycles:          1
  IRQ cleared:     0
  Bytes received:  11
~~~~~~

# M-Bus Postscript

Just in case anyone coming here wants to connect to a meter over M-Bus, you can't connect serial directly into an M-Bus device - it needs stepping up to 34V.  See about halfway down [this page](https://openenergymonitor.org/forum-archive/node/1944.html) for more info.  [otb-iot](http://www.packom.org/otb-iot/) includes some apps to process received M-Bus data into human readable form.