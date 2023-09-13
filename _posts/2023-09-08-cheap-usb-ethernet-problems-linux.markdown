---
layout: post
title:  "Cheap USB Ethernet dongle problems with linux"
date:   2023-09-08 7:02 +0000
tags:   raspberry pi ethernet usb linux
---

I recently moved my main router over from an intel based desktop machine to a Raspberry Pi, in order to lower running costs.  As it's a router I need two ethernet ports, so I added a cheap USB ethernet dongle that I had lying around.  I found that I would get multiple errors per second like this:

```
Sep  4 03:13:04 localhost kernel: [388640.251402] dwc2 3f980000.usb: dwc2_hc_chhltd_intr_dma: Channel 1 - ChHltd set, but reason is unknown
Sep  4 03:13:04 localhost kernel: [388640.274297] dwc2 3f980000.usb: hcint 0x00000002, intsts 0x04600009
Sep  4 03:13:04 localhost kernel: [388640.288388] dwc2 3f980000.usb: dwc2_hc_chhltd_intr_dma: Channel 6 - ChHltd set, but reason is unknown
Sep  4 03:13:04 localhost kernel: [388640.311224] dwc2 3f980000.usb: hcint 0x00000002, intsts 0x06600029
```

Occasionally, maybe once a week, the entire Pi would lock up and need rebooting.  

From searching for similar issues, this seemed like a quite rare problem, but there were other reports of similar issues.  People seemed to conclude that the Pi hardware itself was at fault.

I hit this problem with a Pi 3B+, and found the same problem with multiple different Pis using the same dongle when there was some level of traffic - but no issues with no traffic.

I eventually decided to swap the dongle out for a higher quality (or least more expensive with a recognisable brand) dongle that I had lying around.  The problem then went away.  To me that suggests that there's a problem with the dongle itself, either manufacturing or desig issue.  Maybe badly routed high speed differential pairs on the PCB.

The offending dongle was a TECKNET USB 3.0 to Gigabit Ethernet Adapter with the following details:

```
[188153.213929] usb 2-1: new SuperSpeed USB device number 2 using xhci_hcd
[188153.235145] usb 2-1: New USB device found, idVendor=0bda, idProduct=8153, bcdDevice=31.00
[188153.235172] usb 2-1: New USB device strings: Mfr=1, Product=2, SerialNumber=6
[188153.235189] usb 2-1: Product: USB 10/100/1000 LAN
[188153.235203] usb 2-1: Manufacturer: Realtek
[188153.235217] usb 2-1: SerialNumber: 001000001
[188153.374382] usb 2-1: reset SuperSpeed USB device number 2 using xhci_hcd
[188153.427513] r8152 2-1:1.0: load rtl8153b-2 v1 10/23/19 successfully
[188153.468448] r8152 2-1:1.0 eth1: v1.12.13
[188153.567523] usbcore: registered new interface driver cdc_ether
[188153.570571] usbcore: registered new interface driver r8153_ecm
```