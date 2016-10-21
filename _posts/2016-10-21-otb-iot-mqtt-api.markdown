---
layout: post
title:  "otb-iot MQTT API"
date:   2016-10-21 17:45:00 +0000
categories: esp8266 otb-iot mqtt api config
---

# otb-iot MQTT API

[otb-iot](/otb-iot/) devices are designed to be controlled via an MQTT API.  [MQTT](https://en.wikipedia.org/wiki/MQTT) is a very lightweight [publish/subscribe model](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern) protocol designed for Internet of Things devices, and runs well on the esp8266.  otb-iot's MQTT stack is based on [Tuan PM](https://github.com/tuanpmt)'s excellent [piece of work](https://github.com/tuanpmt/esp_mqtt).

Once the otb-iot device has been configured to connect to a particular WiFi AP, and a particular MQTT server, all further communication with the device is intended to take place over MQTT - so this includes everything from configuration, querying devices stats and sensor state, to resetting the device.  (This initial WiFi and MQTT server config is done by connecting to the AP exposed by the otb-iot device and entering the information into the captive portal.)

I recently reworked the MQTT configuration handling within otb-iot to make it far easier to extend the API in future, and the maintain what's already there.

# API Overview

MQTT supports the concept of topics and messages.  When publishing information you publish a message to a particular topic.  When subscribing, you subscribe to a topic or topics and get messages published to that topic.

Topics within MQTT are hierarchical - they can consist of multiple segments separated by forward slashes "/".  When subscribing you can wildcard at a particular level in the hierarchy, to be delivered all messages for all sub-topics.

## Topics Subscribed to by otb-iot

All otb-iot devices now subscribe to two topics once they have booted, connected to the configured AP, and then to the MQTT server:

~~~~~~
/otb-iot/<chip-id>
/otb-iot/all
~~~~~~

\<chip-id\> is a 6 character string of hex digits such as "01abcd".  This represents the last 3 bytes of the esp8266 MAC address, and is the chip ID returned by the SDK for that device.  

(As an aside I'm not convinced about the uniqueness of the chip ID, as 3 bytes of data = 16M unique IDs - and I've got esp8266s with different OUIs, so presumably chip IDs must be reused.)

To direct a message at a particular otb-iot device you publish it to the /otb-iot/\<chip-id\> topic.

To direct a message at all otb-iot devices you publish it to /otb-iot/all (and all devices should respond).

Any message can be sent to to both the "\<chip-id\>" and "all" topics.

## Message structure when sending to otb-iot 

MQTT doesn't enforce any structure or syntax within the message itself.  otb-iot does - for commands or instructions sent to the otb-iot device, these are partitioned into sub-commands using the same forward slash "/" as MQTT uses to segment topics.

Hence an otb-iot MQTT command looks something like this:

~~~~~~
trigger/ping
~~~~~~

Supported top-level commands are:

* trigger - cause the otb-iot device to do something immediately

* set - change some setting or configuration of the otb-iot device

* get - retrieve some setting, state or value

* delete - delete some setting or configuration

So:

~~~~~~
trigger/ping
~~~~~~

causes the otb-iot device to respond to the ping, which it does with a pong.

## Topics published to by otb-iot

otb-iot sends all status messages and responses to the:

~~~~~~
/otb-iot/<chip-id>/status
~~~~~~

topic.

The following topic is used when sending unsolicited log messages (such as when a serious error is hit by the device).

~~~~~~
/otb-iot/<chip-id>/log
~~~~~~

## Responses from otb-iot

When responding to an incoming message or command, otb-iot will respond using the 

~~~~~~
/otb-iot/<chip-id>/status
~~~~~~

topic.

The message structure here is slightly different to incoming messages - distinct pieces of a message _from_ otb-iot are separate by colons ":".  And messages are sent without spaces, but instead have underscores "_" separating any words from each other.

For example, a response to the ping command would be:

~~~~~~
/otb-iot/<chip-id>/status ok:pong
~~~~~~

# Supported commands

The full, up to date API is documented within otb_cmd.h - and a copy from October 2016 is reproduced here:

~~~~~~
// get
//   sensor
//     temp
//       ds18b20
//         num     
//         value   // Index 0 to 7  !! Unimplemented
//         addr    // Index 0 to 7 
//     adc
//       ads     // ADS1115 family
//     gpio
//       native
//       pcf     // PCF8574  family
//       mcp     // MCP23017 family
//       pca     // PCA9685  family
//   config
//     all
//     ??
//   info
//     version
//     compile_date
//     compile_time
//     boot_slot
//     logs
//       flash   // Unimplemented
//       ram
//     rssi
//     heap_size
//     reason
//       reboot
//     chip_id
//     hw_info
//     vdd33
// set
//   config
//     keep_ap_active
//       yes|true|no|false
//     loc
//       1|2|3
//         <location>
//     ds18b20
//       <addr>  // xx-yyyyyyyyyyyy format
//         <name>
//     ads
//       <addr>  // Should be submitted on its own to initialize an ADS
//         mux
//           <value>
//         rate
//           <value>
//         gain
//           <value>
//         cont
//           <value>
//         rms
//           <value>
//         period
//           <value>
//         samples
//           <value>
//         loc
//           <value>
//   boot_slot
// delete
//   config
//     loc
//       all
//       1|2|3
//     ds18b20
//       all
//       <addr>
//     ads
//       all
//       <addr>
// trigger
//   update
//   upgrade
//   reset
//   reboot
//   ping
//   ow
//     ??
//   i2c
//     ??
//   test
//     led    
//       once   // led name    
//       go     // led name
//       stop   // led name
//  
~~~~~~
