---
layout: post
title:  "RESTful M-Bus Web Server"
date:   2019-03-16 08:02:00 +0000
categories: m-bus mbus rpi raspberry pi restful microservice
---

To make it easier to control the [M-Bus Master Hat](https://www.packom.net/m-bus-master-hat/) for Raspberry Pi I've just released an open source web server which exposes RESTful APIs to manage the Hat and perform common M-Bus operations - [mbus-httpd](https://github.com/packom/mbus-httpd).

[mbus-httpd](https://github.com/packom/mbus-httpd) is written in Rust, and available as a pre-packaged [container](https://hub.docker.com/r/packom/mbus-httpd-release) for both ARMv6 and ARMv7 variants of the Raspberry Pis (which covers all of them).  An x86-64 container is also available.

As well as being able to control the M-Bus Master Hat, [mbus-httpd](https://github.com/packom/mbus-httpd) can also control any M-Bus device which is either
- controlled via the standard Raspberry Pi serial port
- plugs in via a USB port, and is implemented using a USB-serial device (including some USB M-Bus Masters available on aliexpress and ebay).

[mbus-httpd](https://github.com/packom/mbus-httpd) is licensed under the [GPL v3.0 or later](https://github.com/packom/mbus-httpd/blob/master/LICENSE).

See the [README](https://github.com/packom/mbus-httpd) for instructions on building and using [mbus-httpd](https://github.com/packom/mbus-httpd).

[mbus-httpd](https://github.com/packom/mbus-httpd) makes uses of [libmbus](https://github.com/rscada/libmbus) which is licensed under the [BSD 3-clause license](https://github.com/rscada/libmbus/blob/master/LICENSE).