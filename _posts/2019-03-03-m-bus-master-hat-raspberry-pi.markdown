---
layout: post
title:  "Raspberry Pi M-Bus Master Hat"
date:   2019-03-03 17:02:00 +0000
categories: mbus libmbus raspberry pi rpi serial meter m-bus hat
---

<style>
.aligncenter {
    text-align: center;
}
</style>

After a chance comment by a user of [otb-iot](/otb-iot/) to connect to an M-Bus device I decided to develop a Raspberry Pi M-Bus Master "Hat".  A [Raspberry Pi Hat](https://www.raspberrypi.org/blog/introducing-raspberry-pi-hats/) is an add-on board which connects to a Raspberry Pi offering additional functionality.  This M-Bus Master Hat, perhaps unsurprisingly, extends the Raspberry Pi's function making it an M-Bus Master.

This simplies the steps needed to access an M-Bus slave.  With otb-iot you need an MQTT broker, which in turn talks to an ESP8266 device over WiFi, which then connects to an custom developed M-Bus Master bus driver, and you must also implement a separate step to encode and decode the M-Bus protocol data.  With the Raspberry Pi M-Bus Master Hat you only need one device, and this can be driven using the existing open source [libmbus](https://github.com/rscada/libmbus).

<p class="aligncenter">
  <a href="/m-bus/master/main"><img alt="M-Bus Master Hat mounted on a Raspberry Pi Model 3 A+" src="/static/img/mbus_master_and_pi.JPG" width="360" /></a>
</p>

For more details and to order [go here](/m-bus/master/main).