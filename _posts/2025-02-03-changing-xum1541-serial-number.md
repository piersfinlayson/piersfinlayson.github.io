---
layout: post
title: "Setting an xum1541/ZoomFloppy serial number"
date: 2025-02-03 12:00 +0000
tags: 1541 commodore xum1541 serial floppy disk atmel atmega opencbm zoomfloppy
---

The xum1541 (aka ZoomFloppy) is a nifty device which allows you to connect your Commodore disk drives to your PC (Windows, Linux, MacOS).  It connects to your PC via USB and exposes a serial (IEC), parallel or IEEE-488 bus for you to connect your disk drives.

If you want to connect multiple xum1541s to your PC, in order to have multiple buses you can - you just need xum1541s with different serial numbers.  However, there's a problem with this - there's no obvious, supported or easy mechanism to create an xum1541 with a serial number other than 0.

Why would you want multiple?
* to have both an IEC bus and IEEE-488 from one PC
* to connect more devices than one bus can support
* to connect multiple devices with the same numbers simultaneously.

The only way I'd seen to do previously this was to change the firmware flashed to the device.  I've now found an easier way (on linux) which does not require modifying the main firmware.

The mechanism involves writing a single byte to the eeprom area of the ATMEGA processor.  However it does also require erasing the device and reinstalling (or upgrading) the stock xum1541 firmware.

This is possible because the firmware reads the serial number from the first byte of the eeprom (and as far as I can see, none of the rest of the eeprom is used for any purpose).  If the eeprom is unset it will be 0xff (all 1s).  The firmware than does a bitwise NOT operation (~) on the serial number it reads, hence an unwritten eeprom byte 0 because serial number 0.

Instructions follow.  However, as there's a chance of bricking your device doing this, continue at your own risk.

## Pre-requisites

There are three pre-requisites

* You will need to source the latest xum1541 firmware.  The latest ZoomFloppy variant firmware can currently be found [here](https://github.com/OpenCBM/OpenCBM/blob/master/xum1541/xum1541-ZOOMFLOPPY-v08.hex).

* You will need `dfu-programmer`.  Releases of this are [here](https://github.com/dfu-programmer/dfu-programmer/releases).  Just download the appropriate version, untar it and stick the dfu-programmer binary somewhere useful like `/usr/local/bin/`.

* You will need [serial.py](https://github.com/piersfinlayson/xum1541/blob/main/scripts/serial.py) and `pip install intelhex`.

## Re-programming

Put the xum1541 in DFU mode.  This is usually done by pressing the button on the xum1541.  You can verify it's in DFU mode by running `lsusb` - you should see something like this

```
Bus 001 Device 067: ID 03eb:2ff0 Atmel Corp. atmega32u2 DFU bootloader
```

Then run the following commands - if your xum1541 has a different atmega chip (see the lsusb output), change the variant string in the `dfu-programmer` commands.

```
python3 serial.py  # Then enter the serial number you want, between 0 and 255

dfu-programmer atmega32u2 erase --force

dfu-programmer atmega32u2 flash --eeprom eeprom-serial.hex  # eeprom-serial.hex is the file serial.py produced

dfu-programmer atmega32u2 flash xum1541-ZOOMFLOPPY-v08.hex  # or whatever firmware you want to flash

dfu-programmer reset
```

Now when you run `lsusb` you should see something like:

```
Bus 001 Device 068: ID 16d0:0504 MCS RETRO Innovations ZoomFloppy
```

Note that if you're using `usbipd` to attach the xum1541 to WSL, you will need to rerun the `usbipd bind` command, and then re-reun `usbipd attach` as it will see the device with a different serial number as a new device.  If you have no idea what `usbipd` or WSL are, you can safely skip this step. 

Get the bus ID and device ID from the previousl `lsusb` command - in my case it's 1:68.  Now run `lsusb -v -s <this value>`.  You should see a long output including 

```
...
  iSerial                 3 001  # Serial number 1, or whatever number you passed to serial.py
...
```

If you hit any problems try disconnecting and re-attaching your xum1541.

With a possible 256 serial numbers and a max of 4-5 drives per device ... well that should keep you going for some time!

## Other musings

`xum1541cfg` which ships with [OpenCBM](https://github.com/OpenCBM/OpenCBM) purports to support setting a serial number, but indicates this is "currently unsupported".

After much experimentation I don't think the eeprom on these ATMEGA chips can be written, at least via USB, after the device has been flashed.  Hence you need to go through the process above - erase the entire device, program the flash, then program the firmware (which then locks the eeprom for writing). 

Therefore I don't think this `xum1541cfg` command line option can really work (unless it read in the firmware, stored it, erased the device, flashed the eeprom, then reflashed the firmware - which is then obviously prone to hitting an error at any stage).

It may be that with an ATMEGA programming device and `avrdude` this is possible, but I don't have such a device to check.

It would be possible to enhance the main firmware update mechanism, `xum1541cfg update`, which flashes the firmware (and uses a version of the dfu-programmer code under the covers) to take an optional serial number, and flash the eeprom with it, before flashing the firmware, as it has to erase the device before flashing the firmware anyway.