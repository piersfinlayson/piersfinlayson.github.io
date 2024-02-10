---
layout: post
title:  "My Raspberry Pi Horde"
date:   2024-02-10 7:01 +0000
tags:   raspberry pi horde
---

I thought it would be interesting, for me if nobody else, to do an inventory of all of my Raspberry Pis (not including Picos) - both those that are deployed for various purposes, and those which are unused.  Turns out I have a total of 17 deployed Pis, 27 currently unused, for a total of 44 (and 2 more that I've killed over the years) - seems like a lot!

<figure>
  <img alt="Some Raspberry Pis" src="/static/img/unused_pis_feb_24.jpg" width="480" />
  <figcaption>Unused Pis, clockwise from top left:</figcaption>
  <figcaption>Zeros</figcaption>
  <figcaption>Pi 4s</figcaption>
  <figcaption>CM4s</figcaption>
  <figcaption>Pi 5s</figcaption>
  <figcaption>Pi 3s</figcaption>
</figure>

## Deployed Pis

The oldest deployed Pi is a Model B Rev 1, with 256MB RAM and the 26-pin GPIO header and which was released in 2012.  This has been deployed in a loft driving a USB webcam, as part of my home security system for more years than I can remember - probably closed to 10.  It's very slow and struggles with doing much of anything other than successfully running [motion](https://github.com/Motion-Project/motion), streaming the camera images to a remote browser.

The second oldest Pi is a Model B Rev 2, with 512MB RAM.  Again this has the 26-pin GPIO header.  This is my main internal backup server with 4 USB HDDs attached.

I have one original (non WiFi) Pi Zero deployed, a Rev 1.3.  As it's a Rev 1.3 it's probably not one I picked it up at WHSmiths at Birmingham International railway station with a copy of [MagPi](https://www.theguardian.com/technology/2015/nov/26/raspberry-pi-zero-computer-cheap-free-magazine-magpi) back in 2015.  (I remember going back later for another copy - despite it selling out all over the place, there didn't seem to be many SBC aficionados checking out Smiths at Birmingham International at the time).  This has a Ralink MT7601U WiFi USB dongle installed, and is part of my home monitoring setup, with 2 x DS18B20 one wire temperature sensors, one detecting the outside temperature (reporting -0.1C as I write this), and the other, the temperature in an outbuilding.  This has been deployed for about a year.  The bulk of my home automation and monitoring uses custom ESP8266-based hardware, which I [designed](https://github.com/piersfinlayson/otb-iot/blob/master/docs/source/espi.rst), built and developed the [software](https://github.com/piersfinlayson/otb-iot) for.  (One of the custom hardware variants being Pi Zero form factor and with an almost Pi compatible GPIO header, and which I thought I was very clever in naming the ESPi - pronounced "ee-es-pi".)  However, maintaining the hardware and software for the ESPi is a bit of a pain, so I'm moving over to Pi as devices are damaged, fail, or become unreliable.

I have 6 other Pi Zeros deployed, all W Rev 1.1s:

* Two of these control separate underfloor heating installations.  One of these is very basic, monitoring room temperatures via influxdb queries (my temperature sensors store temperatures to influxdb every minute either directly, or in some cases via an MQTT broker).  It then turns an UFH pump on and off via an off the shelf relay hat, using a python script.  (That room is currently 17.8C, with the floor at 25.8C and the UFH pump on).  This Pi replaced one of my own pieces of hardware (one of my very first ESP8266 designs) about a year ago, to make it more maintainable and reliable.  The second heating Pi is installed on a custom designed central heating PCB, with onboard relays and ports to terminate DS18B20 one wire temperature sensors directly.  This both senses temperatures associated with this UFH installation, storing the results influxdb, and also controls an UFH pump, and diverter valve, via separate relays.  This Pi has been in place since commissioning this UFH installation, around 2 years ago.

* The third Pi Zero W is connected to the heat meter which is part of my 80kW wood fired heating installation.  This installation was originally eligible for a UK government subsidy, so I had to record the heat generated with an approved meter, which supported the M-Bus (Meter-Bus) protocol for remote reading - and obviously this was preferable to using my legs to visit the boiler house to read the meter.  I ended up developing a Pi Hat to support M-Bus, the [M-Bus Master Hat](https://www.packom.net/product/m-bus-master-hat/) which, unlike many (most?) Hats, is fully compliant to the [original Raspberry Pi Hat specification](https://github.com/raspberrypi/hats).  Somewhat embarrassingly I only moved to using a Pi and the Hat I sell about a year ago, retiring the original cobbled together hardware (which was the inspiration for the Hat) that lasted around 7 years and was still going strong.

* Then I have 2 Prusa 3D printers, both controlled by Pi Zero Ws running Octoprint, one with a Pi camera attached.  Despite the dire warnings from Octoprint I've never hit a problem controlling these printers with Pi Zeros.  One of these Pis is connected via USB to the printer, the other soldered directly to the Prusa control board.

* I also have a Pi Zero W (why I'm using the W for this I'm not sure!) emulating a Commodore 1541 disk drive, using a Pi1541 hat and the [Pi1541 software](https://github.com/pi1541/Pi1541).  I use this with my VIC-20s and C64s.

Moving on from the Zeros, I use a Raspberry Pi 3 A+ as a commissioning and test device for the M-Bus Master Hats which I sell.  I have these Hats manufactured for me in China, but as the testing requires M-Bus meters I put them through their paces at home, and also program the EEPROM so the Hats can be detected automatically by the Pi.  I really like the smaller form-factor of the A+, but given sales of the cases I sell alongside the Hats, they do not seem to be very popular generally.


<figure>
  <img alt="Some Raspberry Pis" src="/static/img/pi_servers_feb_24.jpg" width="480" />
  <figcaption>Top Left: Spare equipment and instructions for when lighting (literally) strikes (again) and blows up the DSL modem (again++)</figcaption>
  <figcaption>Top Right: Pi 3 B+ router/firewall and 2 Pi 4 servers (all behind noctua fan), plus DSL modem</figcaption>
  <figcaption>Bottom left: Pi Model B Rev 2 backup server</figcaption>
  <figcaption>Bottom right: Pi CM4 NAS</figcaption>
</figure>

My main router, firewall and reverse HTTP proxy is a Raspberry Pi 3 B+.  As I only have under 20MBbps downstream bandwidth and less than 5MBps upstream I don't need anything more powerful for this application.

I run 2 x Raspberry Pi 4 Bs, one as an external server, and other as an internal server.  The external one runs a number of websites (8 at the moment), plus a (non-mining!) full [bitcoin node](https://github.com/piersfinlayson/bitcoin-docker).  There's a 1TB USB3 SSD attached for the bitcoin blockchain.  The internal server runs an nginx reverse HTTP proxy for my internal web servers, the [mosquitto MQTT broker](https://github.com/eclipse/mosquitto), both an internal docker registry and proxy, influxdb, grafana, and various central home automation tools (like the script which takes temperatures reported over MQTT by my custom hardware and stores in influxdb).  This internal server has a 1TB SSD for the docker registry and proxy storage.  The external server is a rev 1.4 with 8GB RAM (the bitcoin node being a memory hog), and the internal server is rev 1.5 with 4GB RAM.

I also have a Raspberry Pi 4 Compute Module Rev 1.1 with 4GB RAM, an 8GB eMMC and WiFi as a NAS.  This uses a Waveshare carrier (CM4-IO-BASE-C I believe), and has a PCIe M.2 5xSATA board attached, connecting 5 external drives (with a total of around 15TB usable space, mostly in RAID1 configurations).  It also has a 64GB USB SSD with /var mounted, given the small eMMC on this device (CMs were hard to get when I procured this device, so I had to put up with what I could get).  I may upgrade this to a Pi 5 with M.2 Hat in the future.  I've never found a satisfactory media server software package to stream videos with built-in Samsung SmartTV support.  I'm currently using embyserver, but that struggles with this hardware setup with some uncompressed Blu-ray mkvs (not to mention I'd rather be using a non-commercial solution).

I have another Raspberry Pi 4 Rev 1.5 4GB which acts as a build server, and runs 24x7 (although I use it rarely).  This is augmented by a Raspberry Pi 4 (Rev 1.1 1GB), as "play" device, for progressing random projects.  Again I use this rarely, but it's typically left running.

Finally I recently set up a monero node to explore that crypto-currency, on a Raspberry Pi 5 Model B Rev 1.0, with 4GB RAM.  This has a 1TB USB SSD attached to store the Monero blockchain.

I make that 17 Pis that are actively being used, or at least powered on.

## Unused Pis

<figure>
  <img alt="Some Raspberry Pis" src="/static/img/unused_pis_feb_24.jpg" width="480" />
  <figcaption>Unused Pis, clockwise from top left:</figcaption>
  <figcaption>Zeros</figcaption>
  <figcaption>Pi 4s</figcaption>
  <figcaption>CM4s</figcaption>
  <figcaption>Pi 5s</figcaption>
  <figcaption>Pi 3s</figcaption>
</figure>

I have a fine stash of unused Pi Zeros:
* 3 x Pi Zeros (2 x v1.2s which were probably sourced on the front of MagPis in 2015, and 1 x v1.3)
* 4 x Pi Zero Ws (one of which I [modded](https://hackaday.com/2017/03/07/adding-an-external-antenna-to-the-raspberry-pi-zero-w/) to support an external WiFi antenna)
* 6 x Pi Zero W 2s

I have a number of unused Pi 3s:
* 4 x 3 A+s
* 1 x 3 B+

I have 3 Pi 4 Bs:
* 1 x 4B 2GB
* 2 x 4B 4GB
* 1 x 4B 8GB

Some spare Compute Module 4s:
* 2 x 1GB, lite, WiFi
* 1 x 2GB, 32GB eMMC, WiFi
* 1 x 8GB, 16GB eMMC, WiFi
* (And a spare Waveshare CM4-IO-Base-B)

And ~~a partridge in a pear tree~~ 1 x 8GB Pi 5.

That's 27 total.

I've killed a couple of Pis over the years, and discarded these.  One of the killed device was a Pi 3 A+ and the other I don't have records of.
