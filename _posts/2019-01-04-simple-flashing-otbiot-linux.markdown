---
layout: post
title:  "Simple flashing of otbiot on linux"
date:   2019-01-04 17:24:00 +0000
categories: otbiot esp8266 linux flash docker containers
---

I recently added a simple mechanism for beginners to flash [otbiot](https://otb-iot.readthedocs.io/en/latest/)  onto an ESP8266 device.  It doesn't require downloading and building the [esp-open-sdk](https://github.com/pfalcon/esp-open-sdk) or [otb-iot source code](https://github.com/piersfinlayson/otb-iot) yourself.

Plug your ESP8266 device into a USB port on your linux machine (or, if you're using VirtualBox, [map the USB device](https://www.eltima.com/article/virtualbox-usb-passthrough/) through from your host to your guest).

Then run:

```
dmesg | grep usb
```

You should see output like this (in this example I am using a Wemos D1 mini - the precise text with vary depending on the USB TTL device you are using):

```
[90279.476382] usbcore: registered new interface driver usbserial_generic
[90279.476412] usbserial: USB Serial support registered for generic
[90279.480721] usbcore: registered new interface driver ch341
[90279.480755] usbserial: USB Serial support registered for ch341-uart
[90279.481709] usb 2-1.8: ch341-uart converter now attached to ttyUSB1
```

Note the value provided right at the end - here *ttyUSB1* - you'll need this in a sec.


Install docker if not already installed:

```
curl https://get.docker.com/|sh
```

You may need to log out and log back in again at this point so that your user is part of the docker group.

Run the container containing pre-built otb-iot images.  Change \<usb-device\> to the value you noted earlier - in my example this would be *ttyUSB1*:

```
docker run --rm -ti --device /dev/<usb-device>:/dev/ttyUSB0 piersfinlayson/otbiot
```

Once the container has been pulled and run, Flash the device and connect to it over serial:

```
make flash_initial && make con
```

Use Ctrl-] to terminate the serial connection.

When you want to terminate the container run:

```
exit
```

