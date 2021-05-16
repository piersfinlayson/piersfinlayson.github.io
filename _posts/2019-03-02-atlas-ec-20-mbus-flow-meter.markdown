---
layout: post
title:  "Atlas EC-20 M-Bus water/flow meter"
date:   2019-03-02 15:32:00 +0000
categories: mbus libmbus raspberry pi rpi serial meter m-bus
---

I recently acquired an [Atlas EC-20 water/flow meter](http://www.atlassayac.com/sayfa/149/ec-20.html) which supports the [M-Bus](http://www.m-bus.com/) protocol for remote reading.

The Atlas EC-20 meter has a default M-Bus address of 48 (0x30) and a default baud rate of 2,400.

The M-Bus command to read this device's M-Bus data is, as hex bytes:

```
10 5B 30 8B 16
```

A sample response, again as hex bytes:

```
68 3D 3D 68 08 30 72 15
73 13 30 93 06 01 04 0E
00 00 00 0C 06 00 00 00
00 0C 14 05 00 00 00 0C
22 33 06 03 00 0C 2E 01
00 00 00 0C 3B 00 00 00
00 0A 59 01 00 0A 5D 01
00 0A 61 01 00 42 6C 7C
22 C8 16
```

This is decoded by [libmbus](https://github.com/rscada/libmbus) as:

```
<?xml version="1.0" encoding="ISO-8859-1"?>
<MBusData>

    <SlaveInformation>
        <Id>30137315</Id>
        <Manufacturer>ATS</Manufacturer>
        <Version>1</Version>
        <ProductName></ProductName>
        <Medium>Heat: Outlet</Medium>
        <AccessNumber>14</AccessNumber>
        <Status>00</Status>
        <Signature>0000</Signature>
    </SlaveInformation>

    <DataRecord id="0">
        <Function>Instantaneous value</Function>
        <StorageNumber>0</StorageNumber>
        <Unit>Energy (kWh)</Unit>
        <Value>0</Value>
        <Timestamp>2019-03-02T15:41:02</Timestamp>
    </DataRecord>

    <DataRecord id="1">
        <Function>Instantaneous value</Function>
        <StorageNumber>0</StorageNumber>
        <Unit>Volume (1e-2  m^3)</Unit>
        <Value>5</Value>
        <Timestamp>2019-03-02T15:41:02</Timestamp>
    </DataRecord>

    <DataRecord id="2">
        <Function>Instantaneous value</Function>
        <StorageNumber>0</StorageNumber>
        <Unit>On time (hours)</Unit>
        <Value>30633</Value>
        <Timestamp>2019-03-02T15:41:02</Timestamp>
    </DataRecord>

    <DataRecord id="3">
        <Function>Instantaneous value</Function>
        <StorageNumber>0</StorageNumber>
        <Unit>Power (kW)</Unit>
        <Value>1</Value>
        <Timestamp>2019-03-02T15:41:02</Timestamp>
    </DataRecord>

    <DataRecord id="4">
        <Function>Instantaneous value</Function>
        <StorageNumber>0</StorageNumber>
        <Unit>Volume flow (m m^3/h)</Unit>
        <Value>0</Value>
        <Timestamp>2019-03-02T15:41:02</Timestamp>
    </DataRecord>

    <DataRecord id="5">
        <Function>Instantaneous value</Function>
        <StorageNumber>0</StorageNumber>
        <Unit>Flow temperature (1e-2 deg C)</Unit>
        <Value>1</Value>
        <Timestamp>2019-03-02T15:41:02</Timestamp>
    </DataRecord>

    <DataRecord id="6">
        <Function>Instantaneous value</Function>
        <StorageNumber>0</StorageNumber>
        <Unit>Return temperature (1e-2 deg C)</Unit>
        <Value>1</Value>
        <Timestamp>2019-03-02T15:41:02</Timestamp>
    </DataRecord>

    <DataRecord id="7">
        <Function>Instantaneous value</Function>
        <StorageNumber>0</StorageNumber>
        <Unit>Temperature Difference (1e-2  deg C)</Unit>
        <Value>1</Value>
        <Timestamp>2019-03-02T15:41:02</Timestamp>
    </DataRecord>

    <DataRecord id="8">
        <Function>Instantaneous value</Function>
        <StorageNumber>1</StorageNumber>
        <Unit>Time Point (date)</Unit>
        <Value>2019-02-28</Value>
        <Timestamp>2019-03-02T15:41:02</Timestamp>
    </DataRecord>

</MBusData>
```
