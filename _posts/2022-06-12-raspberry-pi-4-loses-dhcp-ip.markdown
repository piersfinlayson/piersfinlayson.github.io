---
layout: post
title:  "Raspberry Pi 4 (64-bit) loses DHCP IP address"
date:   2022-06-12 7:00 +0000
tags:   linux raspberry pi dhcp dhcpd
---

Hit an annoying problem whereby a Raspberry Pi 4 running 64-bit (aarch64) Raspbian lite would lose its ethernet and/or wifi IPv4 addresses and not recover them - leading to a dead duck Pi.  As I was setting up this Pi to run some external web servers (to which I want to provide 24x7 access), and it's running headless this wasn't ideal.

I couldn't see any relevant logs in syslog.

I originally though this was a power supply problem so changed cable and power supply.

I then suspected a dodgy SD card, but as I didn't have a spare of the right capacity lying around I swapped to another Pi 4.  The problem recurred on the other Pi 4 - again, leading me to suspect SD card.

However while I was waiting for Amazon to deliver some more 32GB SD cards, I stumbled across a [reddit thread](https://www.reddit.com/r/selfhosted/comments/pkeqh7/raspberry_pi_4_randomly_dropping_wired_network/) reporting that they'd hit a similar problem on a Pi 4 running 64-bit raspbian (lite).  Their workaround was to statically allocate the IP on the Pi rather than use DHCP.  I gave eth0 a static IP.  An hour or so later wlan0 lost its IPv4 address, but eth0 retained it.  

So I statically allocated both the eth0 and wlan0 IPv4 addresses in the /etc/dhcpcd.conf (DHCP client) config file manually like this:

```
interface eth0
static ip_address=192.168.0.232/24
static routers=192.168.0.2
static domain_name_servers=192.168.0.2
static domain_name=internal.packom.net
static domain_search=internal.packom.net

interface wlan0
static ip_address=192.168.0.233/24
static routers=192.168.0.2
static domain_name_servers=192.168.0.2
static domain_name=internal.packom.net
static domain_search=internal.packom.net
```

Note the domain_name and domain_search fields, so that DNS lookups on my internal network work without providing the FQDN.

Current linux kernel version:

```
5.15.32-v8+ #1538
```

Docker version:

```
Docker version 20.10.17, build 100c701
```

I don't see this on another Pi 4 with 64-bit Raspbian lite (although it's not doing very much at present).  I also don't see it on a Pi 4 with 32-bit Raspbian lite (which has been running 24x7 for months).  All the Pis running the same version of docker.  The 64-bit Pi 4 running the same kernel - the 32-bit one obviously running a slightly different version.