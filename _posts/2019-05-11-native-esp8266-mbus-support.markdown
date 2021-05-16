---
layout: post
title:  "Native M-Bus support on the ESP8266"
date:   2019-05-11 12:57 +0100
tags:   esp8266 mbus m-bus libmbus
---

[otb-iot](https://otb-iot.readthedocs.io/en/latest/mbus.html) for the ESP8266 has long supported communicating with M-Bus devices, by providing a hex byte send/receive function over MQTT.  This allows you to give otb-iot the byte data to send on the M-Bus and query otb-iot for the bytes (hopefully) sent in response by a slave.  I enhanced a fork of [libmbus](https://github.com/piersfinlayson/libmbus) to process to this received byte data on a separate machine and format the output as human readable XML.

I've now done an [initial port of libmbus](https://github.com/packom/espi-mbus) itself to the ESP8266.  This means that the construction of the query data and processing of the response into human readable output is all done on the ESP8266, along with actually sending and receiving the data.

Here's some output from the ESP8266's serial port of [espi-mbus](https://github.com/packom/espi-mbus) running on an [ESPi](https://piers.rocks/2019/05/07/introducing-the-ESPi.html) driving an [M-Bus Master Hat](https://www.packom.net/m-bus-master-hat/) connected to an Atlas flow meter.

```
MBUS: Initialize M-Bus library
MBUS: Set up serial port
SOFTUART initialize gpio
SOFTUART bit_time is 417
SOFTUART TX INIT DONE
SOFTUART RX INIT DONE
SOFTUART INIT DONE
MBUS: Set baudrate
MBUS: Init slaves
MBUS: Send request
MBUS: Sent request
MBUS: Receive response
MBUS: Parse frame
MBUS: Generate XML
<?xml version="1.0" encoding="ISO-8859-1"?>
<MBusData>

    <SlaveInformation>
        <Id>0</Id>
        <Manufacturer>ATS</Manufacturer>
        <Version>1</Version>
        <ProductName></ProductName>
        <Medium>Heat: Outlet</Medium>
        <AccessNumber>64</AccessNumber>
        <Status>0</Status>
        <Signature>00</Signature>
    </SlaveInformation>

    <DataRecord id="0">
        <Function>Instantaneous value</Function>
        <StorageNumber>0</StorageNumber>
        <Unit>Energy (kWh)</Unit>
        <Value>0</Value>
    </DataRecord>

    <DataRecord id="1">
        <Function>Instantaneous value</Function>
        <StorageNumber>0</StorageNumber>
        <Unit>Volume (1e-2  m^3)</Unit>
        <Value>5</Value>
    </DataRecord>

    <DataRecord id="2">
        <Function>Instantaneous value</Function>
        <StorageNumber>0</StorageNumber>
        <Unit>On time (hours)</Unit>
        <Value>32312</Value>
    </DataRecord>

    <DataRecord id="3">
        <Function>Instantaneous value</Function>
        <StorageNumber>0</StorageNumber>
        <Unit>Power (kW)</Unit>
        <Value>1</Value>
    </DataRecord>

    <DataRecord id="4">
        <Function>Instantaneous value</Function>
        <StorageNumber>0</StorageNumber>
        <Unit>Volume flow (m m^3/h)</Unit>
        <Value>0</Value>
    </DataRecord>

    <DataRecord id="5">
        <Function>Instantaneous value</Function>
        <StorageNumber>0</StorageNumber>
        <Unit>Flow temperature (1e-2 deg C)</Unit>
        <Value>1</Value>
    </DataRecord>

    <DataRecord id="6">
        <Function>Instantaneous value</Function>
        <StorageNumber>0</StorageNumber>
        <Unit>Return temperature (1e-2 deg C)</Unit>
        <Value>1</Value>
    </DataRecord>

    <DataRecord id="7">
        <Function>Instantaneous value</Function>
        <StorageNumber>0</StorageNumber>
        <Unit>Temperature Difference (1e-2  deg C)</Unit>
        <Value>1</Value>
    </DataRecord>

    <DataRecord id="8">
        <Function>Instantaneous value</Function>
        <StorageNumber>1</StorageNumber>
        <Unit>Time Point (date)</Unit>
        <Value>2019-5-8</Value>
    </DataRecord>

</MBusData>
```

The port is fairly rough and ready at the moment, with various limitations:

* Lots of large statically allocated _and_ dynamically allocated buffers are used by libmbus, meaning it won't co-exist nicely with other RAM hungry applications.

* Doesn't handle sensible formatting of times/dates as there's no native time support in the ESP8266.

* Various other XML output formatting issues (as the ESP8266 SDK doesn't support as rich C format specifiers as other platforms).

* I've found various places (bugs) in libmbus where it's returning and using stack buffers further up the stack.
