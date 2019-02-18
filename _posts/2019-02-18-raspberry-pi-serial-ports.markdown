---
layout: post
title:  "Raspberry Pi Multiple Serial Ports"
date:   2019-02-18 17:32:00 +0000
categories: raspberry pi rpi serial uart pl011 16550 mini zero bcm2835 zerow
---

I've spent some time recently digging into serial port operation on the Raspberry Pi Zero (actually the ZeroW).  This uses the BCM2835 chipset, as do the Raspberry Pi Models A, B, B+, and the Compute Module.

The BCM2835 comes with 2 built in UARTs - the PL011 UART and the mini UART - and these are described in more detail in the BCM2835 [datasheet](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bcm2835/BCM2835-ARM-Peripherals.pdf).

These 2 UARTs have quite different properties, with the mini UART being much more basic.  I need to use the PL011 UART as I need parity support, which the mini UART doesn't have, but PL011 does.  If you want to understand what I was trying to do, see [here]({% post_url 2019-02-18-change-linux-serial-port-speed-and-settings %}).

To use a UART on the Pi, the easiest way is to use raspi-config, disabling the login shell, and enabing the hardware serial support.  This:
* adds enable_uart=1 to /boot/config.txt
* removes console=serial0,115200 (or similar) from /boot/cmdline.txt

However, this default behaviour of the Pi ZeroW uses the PL011 to drive the bluetooth support, with the mini UART used for the on-board TXD/RXD pins (pins 8/10, GPIOs 14/15).  This means that the device tree mapping is:
* /dev/ttyAMA0 -> bluetooth
* /dev/ttyS0 -> mini UART (on GPIOs 14/15)

You can check whether this is the case by using [wiringPi](http://wiringpi.com/).  Run 

```
gpio readall
```

If the mini UART is enabled physical pins 8/10 will be in mode ALT5.  In this mode /dev/serial0 maps to /dev/ttyS0 (which is the mini UART serial port).

To switch to use the PL011 UART for the serial pins, and the mini UART for bluetooth add the following line to /boot/config.txt

```
dtoverlay=pi3-miniuart-bt
```

After rebooting /dev/serial0 maps to /dev/ttyAMA0 which is the PL011 UART.  /dev/serial1 now maps to /dev/ttyS0 (the mini UART driven bluetooth port).

A few people seem to want to know whether it's possible to use both UARTs driving different pins simultaneously.  It isn't with the regular Pis, as the only GPIOs exposed for PL011 and mini UART are GPIOs 14/15 (so you get one UART or the other).  However, it is possible with the compute module, as this exposes more of the BCM2835 GPIOs.
