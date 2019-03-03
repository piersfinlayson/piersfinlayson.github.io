---
layout: page
title: "M-Bus Master Hat"
permalink: /m-bus/master/main
categories: m-bus mbus raspberry pi master hat
---

<style>
.aligncenter {
    text-align: center;
}
</style>

The M-Bus Master Hat is a add-on board designed for the Raspberry Pi which controls the physical layer of an [M-Bus](http://www.m-bus.com/).  It can be used in conjunction with a [Raspberry Pi](https://www.raspberrypi.org/) and software such as [libmbus](https://github.com/rscada/libmbus) to provide a cost effective solution to allow you to connect to and read M-Bus slaves, such as water, heat and electricity meters that implement the wired M-Bus protocol.

<p class="aligncenter">
  <img alt="M-Bus Master Hat mounted on a Raspberry Pi Model 3 A+" src="/static/img/mbus_master_and_pi.JPG" width="360" />
</p>

The M-Bus Master Hat is fully compliant with the [Raspberry Pi Hat specifications](https://github.com/raspberrypi/hats).  It is compatible with any Raspberry Pi which includes the 40 pin header.  This includes all current Raspberry Pi boards, from the Pi 1 Model B+ (2014) onwards, including the Raspberry Pi Zero.

<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top" align="center">
<input type="hidden" name="cmd" value="_s-xclick">
<input type="hidden" name="hosted_button_id" value="J5W8H3YGDZ324">
<input type="image" src="https://www.paypalobjects.com/en_US/GB/i/btn/btn_buynowCC_LG.gif" border="0" name="submit" alt="PayPal – The safer, easier way to pay online!">
<img alt="" border="0" src="https://www.paypalobjects.com/en_GB/i/scr/pixel.gif" width="1" height="1">
<p>(Raspberry Pi Not Included)</p>
</form>

## Getting Started

Instructions on using the M-Bus Master Hat can be found [here](/m-bus/master/instructions).

## Features

* Supports all Raspberry Pi boards from the Raspberry Pi 1 Model B+ (2014) onwards including:

  * Raspberry Pi 1 Model A+.

  * Raspberry Pi 1 Model B+.

  * Raspberry Pi 2 Model B.

  * Raspberry Pi 3 Model A+.

  * Raspberry Pi 3 Model B+.

  * Raspberry Pi Zero.

  * Raspberry Pi Zero W.

  * Raspberry Pi Zero WH.

* Supports up to 3 slave devices connected to device simultaneously.

* Supports up to 100m bus length.

* Supports the following baud rates:

  * 300

  * 600

  * 1200

  * 2400

  * 4800

  * 9600

* Optical isolation between Raspberry Pi and M-Bus.

* Hat and M-Bus powered by Raspberry Pi - no external power supply needed.

* Includes on-board protection to avoid M-Bus from drawing too much power from the Pi.

* Communcates with Raspberrry Pi GPIO serial pins - doesn't use up a USB port.

* Provides a reduced footprint when compared to separate a Pi + USB M-Bus Master solution.

* M-Bus power is controllable via the Raspberry Pi in software.

* Power and M-Bus enabled LEDs.

* Conforms to Raspberry Pi Hat specifications.

* Same form factor as Raspberry Pi 1/3 Models A+.

* Supplied with standoffs to allow the Hat to be securely mounted to the Raspberry Pi.

* Compatible with open source M-Bus master software [libmbus](https://github.com/rscada/libmbus).

## Ordering

Cost is £25 per unit including shipping within the UK.  For shipping to other destinations please [contact me](mailto:mbus@packom.net).

<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top" align="center">
<input type="hidden" name="cmd" value="_s-xclick">
<input type="hidden" name="hosted_button_id" value="J5W8H3YGDZ324">
<input type="image" src="https://www.paypalobjects.com/en_US/GB/i/btn/btn_buynowCC_LG.gif" border="0" name="submit" alt="PayPal – The safer, easier way to pay online!">
<img alt="" border="0" src="https://www.paypalobjects.com/en_GB/i/scr/pixel.gif" width="1" height="1">
</form>

Included:

* One Raspberry Pi M-Bus Master Hat.

* Standoffs and nuts for attaching the Hat to a Raspberry Pi.

* Shipping within the UK.

Not included:

* A Raspberry Pi.

* Any M-Bus slave devices.

* Software, although full instructions are available [here]() for getting [libmbus](https://github.com/rscada/libmbus) running with the Raspberry Pi M-Bus Master Hat.

<p class="aligncenter">
  <img alt="M-Bus Master Hat mounted on a Raspberry Pi Model 3 A+" src="/static/img/mbus_master_on_own.JPG" width="360" />
</p>

## Coming Soon

A Raspbery Pi M-Bus Slave Hat, allowing the Raspberry Pi to operate as an M-Bus slave, will be available by middle 2019.

A Raspberry Pi based M-Bus Master HTTP server compatible with the Raspberry Pi M-Bus Master Hat will be available by middle 2019.

If there is enough interest, it may be possible to produce a Raspberry Pi M-Bus Master Micro-Hat, which would be the same form factor as a Raspberry Pi Zero.  If you are interested in this please [contact me](mailto:mbus@packom.net).

## Attribution

The M-Bus Master Hat is based on an M-Bus Master design available as part of [libmbus](https://github.com/rscada/libmbus).

# libmbus License

BSD 3-Clause License

Copyright (c) 2010-2012, Raditex Control AB
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


