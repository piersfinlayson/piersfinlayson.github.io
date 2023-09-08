---
layout: post
title:  "M-Bus Master on Raspberry Pi Pico"
date:   2023-09-08 7:00 +0000
tags:   raspberry pi pico sdk picotool bare metal docker dockerfile container build mbus master
---

I have a working [M-Bus Master implementation](https://github.com/packom/pico-mbus) on the Raspberry Pi Pico, through a port of [libmbus](https://github.com/piersfinlayson/libmbus) to the Pico C SDK.

The port itself was straightforward - the Pico's [hardware_uart](https://www.raspberrypi.com/documentation/pico-sdk/hardware.html#hardware_uart) API is easy to port to from libmbus's current [termios](https://man7.org/linux/man-pages/man3/termios.3.html) serial implementation.

To build [pico-mbus](https://github.com/packom/libmbus):
* Install the Pico C SDK if you haven't already got it - [pico-build](https://github.com/piersfinlayson/pico-build) provides a simple way of doing this
* Clone and build [pico-mbus](https://github.com/packom/libmbus)

I've tested this, naturally, with the [M-Bus Master Hat](https://www.packom.net/product/m-bus-master-hat/), although it should work with other M-Bus Master hardware serial implementations.

Wiring instructions are given in the [README](https://github.com/packom/pico-mbus/blob/main/README.md).

Here is the Pico output from scanning my M-Bus test rig, with slaves configured at addresses 1, 2 and 48.

```
------------
M-Bus: Start
M-Bus: Turn bus power on
M-Bus: Pause for 1000ms
M-Bus: Create serial context
M-Bus: Connect to serial
M-Bus: Using UART0
M-Bus: Set baudrate to 2400
M-Bus: TX Pin: 0
M-Bus: RX Pin: 1
M-Bus: Set flow control: CTS off RTS off
M-Bus: UART settings: Data 8 Stop 1 Parity 1
M-Bus: Set search retries value to 0
M-Bus: Scanning primary addresses:
Found an M-Bus device at address 1
Found an M-Bus device at address 2
Found an M-Bus device at address 48
M-Bus: Scan complete - results:
       Slaves found:    3
       Collisions:      0
       Addresses found: 1 2 48
M-Bus: Disconnect
M-Bus: Free context
M-Bus: Turn bus power off
M-Bus: Pause for 10000ms before rescanning

```