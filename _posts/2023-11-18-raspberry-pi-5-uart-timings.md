---
layout: post
title:  "Raspberry Pi 5 UART timings different from previous generations"
date:   2023-11-18 7:01 +0000
tags:   raspberry pi 5 uart rp1 rpi5 serial timing mbus master hat
---

*Edit: 29th April 2024 - I no longer believe the Pi 5 UART timings are responsible for the problems I saw with the Pi 5 and serial, as I and others have seen similar problems with earlier versions of the Pi.  Specifically, I have fixed limbus [here](github.com/piersfinlayson/libmbus) by increasing the timeouts.  I suspect instead, changes to the linux kernel (probably in version 6 somewhere).*

It looks like the UART timings, at least for low baud-rate applications, differ substantially on the Raspberry Pi 5 compared with previous generations.

I guess this is down to the RP1 chip, where, on the Raspberry Pi 5, the UARTs (and other peripherals) are implementated on a separate IC to the CPU.  On previous generations, the UARTs are onboard the main processor.

It seems like this increases the delay in receiving serial data, and may render existing code that works on previous generations of the Pi not working, at least not reliably.

I discovered this using a 2400 bps external device.

A workaround/fix is to change the timeouts in your software.  For example:

* termios
  * ```c_cc[VTIME]``` must be increased
* pySerial
  * ```serial.Serial(timeout=X)``` must be increased

For 2400 baud communications I found I needed to increase:
* C/Termios - ```c_cc[VTIME]``` to 5 (from 3, the unit being 1/10s)
* Python - ```timeout``` to 0.55 (from 0.5, the unit being s)

## Detail

The device I'm using is an [M-Bus Master Hat](https://www.packom.net/product/m-bus-master-hat/), and the software both:
* [libmbus](https://github.com/rscada/libmbus)
* [pyMbusHat](https://github.com/packom/pyMbusHat)

These have worked well on all previous generations of the Raspberry Pi.

This use case interfaces with M-Bus slaves, which require even parity, hence the PL011 UART on the Raspberry Pi must be used.  This is the only option on the Raspberry 4 and 5, but on the previous generations, the miniuart (which is the default) cannot be used, as this doesn't support parity settings.  This means that all of my testing has been using the same UART implementation - the PL011.

All Raspberry Pis, including the 5, use a p1r5 verion of the PL011, according to their datasheets.  Hence the hardware UART implementation should be identical between my tests.

libmbus uses termios for serial communication, and sets the ```c_cc[VTIME]``` field to 3 when baud-rate is 2400.  This is [how many tenths of a second](http://unixwiz.net/techtips/termios-vmin-vtime.html) termios will wait after a character burst to see if any more characters arrive, before a read returns.

Testing libmbus on the Raspberry Pi 5, with the same M-Bus Master Hat and same slaves as on previous generations of the Pi, leads to communicating failing consistently with 2 out of the 3 slaves, with the existing ```c_cc[VTIME]``` settings.  Increasing ```c_cc[VTIME]``` from 3 to 5 consistently fixed the problem.

Similarly using pyMbusHat, which uses pySerial for serial communications, the communication consistently fails with some of the slaves with the current timeout setting of 0.5 (s), with it consistently working when it is set ot 0.55.

## Fixing libmbus

Edit ```mbus/mbus-serial.c```.  In function ```mbus_serial_set_baudrate```, within ```case 2400:``` change:
```
serial_data->t.c_cc[VTIME] = (cc_t) 3;
```
To:
```
serial_data->t.c_cc[VTIME] = (cc_t) 5;
```

Save and rebuild libmbus.

## Fixing pyMbusHat

I have committed a fix to the [master repo](https://github.com/packom/pyMbusHat).

## Using the M-Bus Master Hat with a Pi 5

If you found this article trying to figure out how to get an M-Bus Master Hat working on the Raspberry Pi 5, as well as modifying the software as above, you will need to follow these instructions.

Add this to the end of your ```/boot/config.txt```:
```
dtoverlay=uart0-pi5
```

Reboot, and then to turn on the M-Bus power:
```
pinctrl set 26 op
pinctrl set 26 dh
```

Like on previous generations of the Pi, the serial device to use is ```/dev/ttyAMA0```.