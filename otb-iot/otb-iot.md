---
layout: page
title:  "otb-iot"
permalink: /otb-iot/
---

# Out of the Box - Internet of Things

## Introduction

[otb-iot](https://piersfinlayson.github.io/otb-iot/) is software for ESP8266 devices which is intended to make the ESP8266 quick and easy to deploy for _real_ applications, and to be _robust_.

There's a huge amount of hacking and playing going on with the ESP8266 today, which is a fantastic thing for all hobbyists, enthusiasts and those looking to develop deployable products.  But while it's very quick and easy to get stuff running on the ESP8266, and even to cobble together something that provides a lot of function, making it fully featured enough to actually deploy and maintain in the field takes effort.

This is where otb-iot comes in - it's a complete software image for the ESP8266 which is intended to be this robust and deployable solution.

## Getting Started

I've tried to make it as easy as possible to get started.  There are five main steps:

* Install the [open-esp-sdk](https://github.com/pfalcon/esp-open-sdk)
* (Optional) Install [platformio](http://platformio.org/#!/get-started)
* Clone the otb-iot software from [github](https://github.com/piersfinlayson/otb-iot)
* Build it
* Install it

I strongly recommend using linux as the build environment.  If like me you won't touch a linux desktop environment with a barge-pole you may want to run linux as a virtual machine within a hypervisor such as [VirtualBox](https://www.virtualbox.org/), and then ssh into it from your Windows or Mac.

### open-esp-sdk

The simple instructions to install this are [here](https://github.com/pfalcon/esp-open-sdk#requirements-and-dependencies).  It takes me about an hour from scratch to install this piece - as I have pretty slow internet access.

### platformio

This is only used by the otb-iot Makefile to provide convenient serial monitor.  Doubtless there's easier ways to get this function - but I started out using the ESP8266 Arduino framework and platformio is awesome at making this easy.  Follow the CLI instructions [here](http://platformio.org/#!/get-started).

### otb-iot

#### Getting the software

    git clone https://github.com/piersfinlayson/otb-iot.git


#### Building it

* Go to the directory you've cloned otb-iot

      cd otb-iot

* Ensure you expose SDK_BASE from your shell, pointing at the base open-esp-sdk directory - or uncomment this line in the Makefile and make sure it's set correctly:

      # SDK_BASE = /opt/esp-open-sdk

* Check ESP_SDK is set correctly in the Makefile to point to the Espressif SDK within the open-esp-sdk directory:

      ESP_SDK = esp_iot_sdk_v1.4.0

* Run make

      make

#### Installing it

* Plug your ESP8266 to a USB port on your machine - either using the port provided by a dev board like Nodemcu or the WeMos D1-mini, or using a separate FTDI/CH340/etc serial to USB converter.  If you're using linux in a VM you'll need to set up a rule within your hypervisor to route the USB device to the VM.  Note only boards with 4MB (32Mbit) of flash (or greater) are currently supported.  This seems to be all of the current batch of ESP-12s coming out of China at the moment.

* Use make to flash your device:

      make flash_initial

That's it - you should now be up and running

#### Using otb-iot

There's more detailed information later, but in a nutshell to start using otb-iot:
* Connect to the "OTB-IOT.XXXXXX" WiFi Access Point which will now be available.* This should activate captive portal on your device, but if not point a browser at http://192.168.4.1
* Configure
  * Your WiFi credentials (access point SSID and password)
  * Your MQTT server details (IP address and any username/password)
* Hit submit

The ESP8266 will now reboot and should connect to your WiFi network.  The WiFi AP will be exposed at all times to allow you to reconfigure the above details while MQTT isn't connected.  When MQTT is connected by default the AP will turn off, but you can override this behaviour both within the captive portal, and using MQTT if you desire.

You can now start communicating with your ESP8266 over MQTT.  To check it's responding send to topic _/otb_iot/all/system_ message _ping_.  You should get a message _pong_ sent to topic _/otb_iot/all/status_. 

To use mosquitto to send and receive MQTT messages run this command in one shell:

    mosquitto_sub -v -h _your_mqtt_server_ -t 

to listen for all MQTT publishes.

And then in another:

    mosquitto_pub -h _your_mqtt_server_ -t /otb_iot/all/system -m ping
    
to send the ping.  You should see a message like this in response:

    /otb_iot/xxxxxx/status pong

where xxxxxx is the chip ID of your ESP8266.

## IOT Function

Today otb-iot provides the following IOT functionality:

* Support for reporting temperatures from [DS18B20](http://www.hobbytronics.co.uk/ds18b20-arduino) sensors over MQTT

* Ability to set GPIO output to high and low over MQTT

* Access to various management capabity over MQTT including

  * Over the Air (OTA) upgrades
  * Reconfiguration
  * Querying wifi signal strength
  * Querying GPIO status
  * Reset/reboot
  * Retrieving logs and last reboot reason

## Supported boards

Anything with at least 4MB (32MBit) of flash should be supported.  It would probably be possible to squeeze down to 2MB fairly easily, but I've not seen any 2MB boards out there.  As otb-iot includes 3 boot images for robustness, squeezing into 1MB would be problematic.

This means that any recent (early 2016) ESP-12 should work.  Most of my testing has been done with:

* [WeMos D1-mini](http://www.wemos.cc/wiki/doku.php?id=en:start) (my favourite)

* [Nodemcu V3 from LoLin](https://cknodemcu.wordpress.com/2015/11/13/nodemcu-variants/) (a bit big)

To see check your board size run:

    esptool.py flash_id

If you get 4016 reported you're good to go.

## MQTT "API"

I took the decision to use [MQTT](http://mqtt.org/) as the primary communication protocol because
* it's suited to IOT applications due to its lightweight nature (both requiring little footprint for implementation, and having little protocol overhead on messages)
* to keep functionality limited - remember a focus here is to be robust and stable, which is hard with a plethora of function.

Therefore only very limited configuration is available over WiFi/IP.

### Sending and Receiving Messages

To send messages to the otb-iot device, use one of the following topics:

    /otb_iot/all/system - Addresses all otb-iot devices attached to your MQTT broker
    /otb_iot/chipid/system - To just address your device
    /otb_iot/loc1/loc2/loc3/chipid/system - To just address your device, if you've set the loc1, loc2 and loc3 values
    
Regular status updates and responses to messages sent on the system topic will be sent using one of the following topics:

    /otb_iot/chipid/status - if loc1, loc2 and loc3 aren't set
    /otb_iot/loc1/loc2/loc3/chipid/status - if they are set
    
The otb-iot device may also send using one of the following topics when reporting serious errors:

    /otb_iot/chipid/error
    /otb_iot/loc1/loc2/loc3/chipid/error

Temperature readings will be sent once a minute for each attached DS18B20 using:

    /otb_iot/loc1/loc2/loc3/chipid/temp/sensor_loc/sensorid
    
Loc1, loc2 and loc3 will be included only if configured, as will sensor_loc.  All temperature readings are in Celsius, and the DS18B20 claims +-0.5C accuracy.

### System Messages

The support messages are as follows:

To set config values:

    config:set:field:value

Field may be one of:

    ssid      # WiFi SSID
    password  # WiFi Password
    loc1      # Location 1 to use in topics
    loc2      # Location 2 to use in topics
    loc3      # Location 3 to use in topics
    keep_ap_active  # Keep AP active when MQTT connected

To set DS18B20 sensor_loc information:

    config:set:ds18b20:addr:loc  # To set a location
    config:set:ds18b20:clear     # To clear all DS18B20 location information
    
The address format for DS18B20 sensors is 28-112233445566 (not including checksum)

To retrieve config values:

    config:get:field     # Values as above
    config:get:ds18b20s  # To get the number of _configured_ DS18B20s (i.e. locations)
    config:get:ds18b20:addr   # To get DS18B20 info by address
    config:get:ds18b20:loc    # To get DS18B20 info by location
    config:get:ds18b20:slot   # To get DS18B20 by slot - up to 8 (0-7) are supported 

To get info about actual connected DS18B20s (as opposed to configured address/locations):

    ds18b20:get_num          # Gets number of devices connected at last book
    ds18b20:get:ds18b20:num  # Where num starts at 0 and goes up to 7 depending on number of connected - returns address in above format

To retrieve received signal strength of connected AP:

    rssi:get

To get current free heap size of ESP8266:

    heap_size:get

To reset (reboot) the device use either:

    reset
    reboot

To ping the device over MQTT:

    ping

To retrieve last reboot reason:

    reason:reboot

To get otb-iot software version;

    version:get
    
To get ESP8266 chip ID:

    chip_id:get

To get software compile date:

    compile_date:get

To get software compile time:

    compile_time:get

To see which boot slot the software is currently running from:

    boot_slot:get

To set the slot to boot from at next reset:

    boot_slot:set:value  # 0 or 1

To set GPIO value:

    gpio:set:pin_no:value  # value = 0 or 1, pin=2 is reserved for DS18B20s

To apply and save GPIO value so it's applied after next reset (NOT YET IMPLEMENTED):

    gpio:save:pin_no:value

To get current pin value:

    gpio:get:pin_no

To update to new software, which installs in the non-current boot slot and reboots when done:    
    
    update:ip_address:port:path    # Uses HTTP for update
    upgrade:ip_address:port:path   # Uses HTTP for update

To retrieve logs from RAM:

    logs:ram:get:num   # 0 = most recent, 1 is next, 2 is next, etc

To retreive logs from flash where they are stored in the event of a serious problem leading to reboot.  (While storing of logs in this case is supported, retrieving over MQTT is NOT YET IMPLEMENTED):    

    logs:flash:get:num  (0 = most recent, 1 is next, …)
    
### Status Messages

otb-iot will send responses to system messages using status messages.  It may also send unsolicited messages in some cases - like when rebooting after an upgrade.

The messages that may be sent are as follows:

    config:set:ok(:further_info)
    config:set:error(:further_info)
    config:get:ok:value(:further_info)
    config:get:error(:further_info)
    gpio:set:ok(:further_info)
    gpio:set:error(:further_info)
    gpio:get:ok:value
    gpio:get:error(:further_info)
    boot_slot:set:ok(:further_info)
    boot_slot:set:error(:further_info)
    boot_slot:get:ok:value
    boot_slot:get:error(:further_info)
    heap_size:get:ok:value
    heap_size:get:error(:further_info)
    pong(:further_info)
    error(:further_info)
    reset:ok(:further_info)
    reboot:ok(:further_info)
    reset:error(:further_info)
    reboot:error(:further_info)
    update:ok(:further_info)
    update:error(:further_info)
    booted unsolicited
    version:version_id
    build_date:build_date
    build_time:build_time
    chipid:chipid 
    reason:further_info
    offline unsolicited (MQTT Last Will and Testament generated by the MQTTbroker)
    
### Error Messages

In the case of a serious error hit by otb-iot it will attempt to send on the error topic a message containing error details

### Message format

As can be seen colon (:) is used to separate fields and parameters in otb-iot MQTT messages.  Colons are not therefore support in values themselves.

In addition whitespace will not be used - any whitespace characters will be converted to _ before being sent in status or error messages.

## Logging

otb-iot outputs useful logs over serial.  It also has a circular log buffer in RAM which can be queried via MQTT.  In the event of a serious error leading to a reset forced by the otb-iot software this will be written to flash.  In the future this flash region will be queryable via MQTT.

otb-iot logs fall into the following categories:

* ERROR
* WARN
* INFO
* DEBUG (compiled out by default)

## Robustness

A number of approaches are taken to ensuring otb-iot's robustness:

* Starting the WiFi AP if MQTT fails, so WiFi and MQTT details can easily be reconfigured as necessary.

* Hardening of the various function provided, handling error codes, and taking corrective recovery on errors.

* Ongoing checking of internal consistency.

* Substantial logging via serial and access to this over MQTT.

* Ability to query device in an automated fashion over MQTT using provided APIs.

* Limiting the exposed function.

* Checksuming of software images, and fallback to alternative image.

* "Factory" Installed 3rd software recovery image, not upgradeable via OTA to allow recovery.

This is still a work in progress.

## Security

This is a work in progress.  Currently MQTT implementation does not support SSL.  WiFi AP passwords are not logged and are not queryable via APIs.

## Third Party Component Usage

* [pfalcon's Open ESP SDK](https://github.com/pfalcon/esp-open-sdk)

* [Espressif ESP non-RTOS SDK](http://bbs.espressif.com/viewtopic.php?f=46&t=850)

* [tuanpmt's MQTT](https://github.com/tuanpmt/esp_mqtt)

* [raburton's rboot](https://github.com/raburton/rboot) and [Esptool2](https://github.com/raburton/esptool2)

* [Spritetm's esphttpd](https://github.com/Spritetm/esphttpd)

* [Paul Stroffgen's One Wire library](http://www.pjrc.com/teensy/td_libs_OneWire.html)

* [Necromant's adaption of the One Wire library in esp8266-frankenstein](https://github.com/nekromant/esp8266-frankenstein)

## otb-iot License

The otb-iot software is licensed under the [GNU General Public License version 3 (GPLv3)](http://www.gnu.org/licenses/).

All of the original versions of the third party code are licensed under their respective licenses, with any new code licensed under the GPLv3.