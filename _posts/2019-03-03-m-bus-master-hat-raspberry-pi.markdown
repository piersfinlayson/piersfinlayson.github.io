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

Updated: 16 February 2020

[Order one here!](https://www.packom.net/product/m-bus-master-hat/)

After a chance comment by a user of [otb-iot](/otb-iot/) connecting to an M-Bus device I decided to develop a Raspberry Pi M-Bus Master "Hat".  A [Raspberry Pi Hat](https://www.raspberrypi.org/blog/introducing-raspberry-pi-hats/) is an add-on board which connects to a Raspberry Pi offering additional functionality.  This M-Bus Master Hat, perhaps unsurprisingly, extends the Raspberry Pi's function making it an M-Bus Master.

This simplifies the steps needed to access an M-Bus slave.  Just install the Hat, and then follow the [simple instructions](https://www.packom.net/m-bus-master-hat-instructions/) to connect to your slaves.

With otb-iot you need an MQTT broker, which in turn talks to an ESP8266 device over WiFi, which then connects to an custom developed M-Bus Master bus driver, and you must also implement a separate step to encode and decode the M-Bus protocol data.  With the Raspberry Pi M-Bus Master Hat you only need one device, and this can be driven using the existing open source [mbus-httpd](https://github.com/packom/mbus-httpd), [libmbus](https://github.com/rscada/libmbus), or other software.

<p class="aligncenter">
  <a href="https://www.packom.net/product/m-bus-master-hat/"><img alt="M-Bus Master Hat mounted on a Raspberry Pi Model 3 A+" src="https://www.packom.net/wp-content/uploads/2020/02/mbus-master-hat-on-pi-a.jpg" width="360" /></a>
</p>

For more details and to order [go here](https://www.packom.net/product/m-bus-master-hat/).