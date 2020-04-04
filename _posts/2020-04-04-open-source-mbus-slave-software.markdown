---
layout: post
title:  "Open Source M-Bus Slave Software (supports Raspberry Pi)"
date:   2020-04-04 9:00 +0000
tags:   pi mbus m-bus power energy hat master slave serial raspberry pi python
---

During a quick search I couldn't find any open source software implementing an M-Bus slave.  There's [libmbus](https://github.com/rscada/libmbus) for the Master, but no obvious slave implementation I could use for some testing.  So I've written [pyMbusSlave](https://github.com/packom/pyMbusSlave) which is a minimial but complete slave implementation written in Python.

It implements the two mandatory functions required by the [M-Bus specification]([M-Bus documentation](https://m-bus.com/documentation)):
* SND_NKE (used by the Master to scan for Slaves)
* REQ_UD2 (requests the slave's user data 2)

The user data is hard coded using a fixed payload type, but the slave's identification (serial) number and M-Bus address are configurable, and it would be straightforward to modify the user data payload.

Instructions for using are in the [README](https://github.com/packom/pyMbusSlave/blob/master/README.md).