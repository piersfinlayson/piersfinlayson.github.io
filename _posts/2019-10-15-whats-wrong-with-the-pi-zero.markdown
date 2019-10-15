---
layout: post
title:  "What's wrong with the pi zero"
date:   2019-10-15 17:52 +0000
tags:   pi zero mbus m-bus power energy
---

I remember when I first came across the Pi Zero.  In fact I was where I am when I start writing this post - the salubrious surroundings of [Birmingham Internal Railway Station](https://www.nationalrail.co.uk/stations/BHI/details.aspx).  As today, I was then on the way back from my all too frequent visits to North London, perusing the magazines at WHSmiths at the station, when I spotted [The MagPi](https://www.raspberrypi.org/magpi/issues/40/) with a free Raspberry Pi Zero on its cover.  I think it was the launch day and I hadn't known the Pi Zero was coming out.  Naturally I bought a copy of the mag, and got myself a Zero.  Foolishly I didn't buy any other copies of The MagPi, as they rapidly sold out across the country.  

I've never really understood why the Pi Zero isn't more popular.  The Pi Zero W variant (with built-in WiFi) is a more practical version of the original zero that's now available.  As of writing going for £9.30 from the usual scumbags.  For the price it's a very capable, small footprint device, with superb software and hardware support.  Far more practical for and totally capable of many applications than its larger brethren.

Why do I assert that it's not that popular?  Two reasons:

* Stock is and has always been massively constrained.  As of today it's out of stock at one of the most well-known UK Pi stores, and there's always been and still is a limit of one Pi Zero per customer per transaction.  I guess it's not that high margin for the [Raspberry Pi Foundation](https://www.raspberrypi.org/) and if they produce as many as the market desires it'll cannabilise sales of the more expensive options.  I don't think that's a good reason for wasting resources and energy manufacturing and powering higher spec machines.

* I've been selling a [Raspberry Pi Hat](https://github.com/raspberrypi/hats), an [M-Bus Master Hat](https://www.packom.net/m-bus-master-hat/) (which reads certain types of metering devices), for some time now.  I have both [full size](https://github.com/raspberrypi/hats/blob/master/hat-board-mechanical.pdf) and [micro hats](https://github.com/raspberrypi/hats/blob/master/uhat-board-mechanical.pdf).  The former is the size of a Raspberry Pi Model A, and designed to be suitable for Pi As and Bs.  The latter is the same size as a Zero, and designed, not surprisingly, for the Zero.  (Both are hardware compatible with all Pis.)  So far I have not sold a single micro M-Bus Master Hat.  I don't really understand why.  The processing required to read a meter and do something useful with the output - even run a [web server to expose the results](https://github.com/packom/mbus-httpd) - is negligible compared to the computing power available.  And the Pi Zero is less than half the price of a Pi Model A or B.  

What am I missing?  Why is everybody in the world using more expensive, more powerful Pi models when a Zero would do?