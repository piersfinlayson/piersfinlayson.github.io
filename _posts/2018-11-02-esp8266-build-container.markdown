---
layout: post
title:  "An ESP8266 NonOS SDK linux build container for x86-64 and the raspberry pi"
date:   2018-11-02 16:30:00 +0000
categories: esp8266 espressif sdk docker containers
---

I have created an ESP8266 build container, for both x86-64 and ARM architecture machines, including the raspberry pi.  The multi-architecture container is available [here](https://hub.docker.com/r/piersfinlayson/esp8266-build/).  This has support for [V3.0](https://github.com/espressif/ESP8266_NONOS_SDK/releases/tag/v3.0) of the Espressif SDK.  It is built on top of Ubuntu 18.04 for x86-64 and Raspbian Jesse for the pi.

Run the container like this:

```
docker run --rm -ti --name esp8266-build -h esp8266-build \
  -v /link/to/your/code:/home/esp/builds \
  piersfinlayson/esp8266-build
```

or

```
docker run --rm -ti --name esp8266-build -h esp8266-build \
  -v /link/to/your/code:/home/esp/builds \
  piersfinlayson/esp8266-build:3.0.0
```

If you want to access a USB port (to enable flashing to an ESP8266 device) from within the container add a device argument like this:

```
--device /dev/ttyUSB0:/dev/ttyUSB0 
```

So:

```
docker run --rm -ti --name esp8266-build-usb -h esp8266-build0-usb \
  --device /dev/ttyUSB0:/dev/ttyUSB0 \
  -v /link/to/your/code:/home/esp/builds \
  piersfinlayson/esp8266-build
```

The SDK is available at /home/esp/esp-open-sdk/ and the code directory you provide will be under /home/esp/builds/.  When the container starts it prints out the supported SDK version like this:

```
SDK Version 3.0.0
```

The Dockerfile and instructions to build these containers and the manifest which supports multiple architectures is [on github](https://github.com/piersfinlayson/otbiot-docker).