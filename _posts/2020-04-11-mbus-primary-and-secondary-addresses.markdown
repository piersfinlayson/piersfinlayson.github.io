---
layout: post
title:  "M-Bus Primary and Secondary Addresses and accessing using libmbus"
date:   2020-04-11 9:00 +0000
tags:   pi mbus m-bus power energy hat master slave serial raspberry pi primary secondary address
---

This post explains the difference between M-Bus primary and secondary addresses, how to discover and configure them, and how to use libmbus with primary and secondary addresses.

If you want to turn a Raspberry Pi into an M-Bus Master, take a look at the [M-Bus Master Hat](https://www.packom.net/product/m-bus-master-hat/).  There are two variants - one for a full-sized Pi and another for the Pi Zero.

# Primary Addresses

Primary addresses are defined by the [data link layer](https://m-bus.com/documentation-wired/05-data-link-layer) portion of the M-Bus documentation.

Primary addresses are one byte in size, and standard device addresses are between 1-250 inclusive.  Special addresses are also identified:

* 0 is used by some unconfigured devices at manufacture, and are intended to be allocated a value from 1-250 when connected to the M-Bus - either using dip switches or some other implementation specific mechanism.

* 254 is a test broadcast address, and all devices that receive messages for this address should reply.  Collisions will occur with multiple slaves attached to the bus, so this address is intended to be used to determine the address of a single slave attached to the bus.

* 255 is also a test broadcast address, but not devices should reply to messages targeted at address 250.

* 251 and 252 are reserved for future applications (so are unused by the specs at this time).

* 253 is used to indicate that secondary addresses is to be used (and the subsequent payload differs as a result)

Many slaves will indicate their default primary address in documentation.  This is also often viewable or configurable via a display if the device has one.

However, if you don't know a slave's primary address, there are 3 ways to determine it via the M-Bus protocol:

* Scan the bus - which involves sending messages to each possible bus address sequentially looking for a response.

* Use address 254 to retrieve its address (with only this slave connected to avoid collisions).

* Query the slave using its secondary address (more on this below).

[libmbus](https://github.com/rscada/libmbus) has the mbus-serial-scan command to scan the bus.  To scan the bus at baudrate 2400, using device /dev/ttyAMA0 the command is run as follows and provides the displayed output.

```
$ mbus-serial-scan -b 2400 /dev/ttyAMA0
Found a M-Bus device at address 1
Found a M-Bus device at address 2
Found a M-Bus device at address 48
```

As can be seen, this M-Bus has 3 slaves attached, with primary addresses 1, 2 and 48.  To determine which device is connected to each address you can run mbus-serial-request-data to retrieve that device's data.  For example, to find out which device is at address 2:

```
$ mbus-serial-request-data -b 2400 /dev/ttyAMA0 2
<?xml version="1.0" encoding="ISO-8859-1"?>
<MBusData>

    <SlaveInformation>
        <Id>18112914</Id>
        <Manufacturer>GJ_</Manufacturer>
        <Version>1</Version>
        <ProductName></ProductName>
        <Medium>Electricity</Medium>
        <AccessNumber>85</AccessNumber>
        <Status>00</Status>
        <Signature>0000</Signature>
    </SlaveInformation>

    <DataRecord id="0">
        <Function>Instantaneous value</Function>
        <StorageNumber>0</StorageNumber>
        <Unit>Energy (100 Wh)</Unit>
        <Value>0</Value>
        <Timestamp>2020-04-11T09:28:36Z</Timestamp>
    </DataRecord>

</MBusData>
```

Bear in mind that while most slaves default to a baudrate of 2400, M-bus does support other baudrates, so if you can't find your slave using a baudrate of 2400 try other speeds.

Also bear in mind that some devices that claim M-Bus support only support the M-Bus [physical layer](https://m-bus.com/documentation-wired/04-physical-layer), and not the M-Bus data protocol - in which case you will not be able to communicate with it via libmbus.  In this case you probably just want to query the serial port directly.  See [this post](/2020/04/01/reading-kaifa-ma304-meter.html) for an example.

# Secondary Addresses

Secondary addresses are defined by the [network layer](https://m-bus.com/documentation-wired/07-network-layer) of the M-Bus protocol.

These are to solve the problem where either the slave has an unknown primary address or a primary address which clashes with that of other slaves on the same bus.

Secondary devices are addressed using primary address 253, and a secondary address which is 8 bytes long and made up of:

* 4 bytes being the device ID (serial #)

* 2 bytes being the manufacturer's identifier

* 1 byte being the device version

* 1 byte being the device media

The detail of actually addressing secondary devices is abstracted away by libmbus.  To find secondary addresses on a bus use the mbus-serial-scan-secondary tool:

```
$ mbus-serial-scan-secondary -b 2400 /dev/ttyAMA0
Found a device on secondary address 181129145F1D0102 [using address mask 1FFFFFFFFFFFFFFF]
Found a device on secondary address 3013731593060104 [using address mask 3FFFFFFFFFFFFFFF]
Found a device on secondary address 99999999FFFF0102 [using address mask 99FFFFFFFFFFFFFF]
```

It can take a while to do a full scan of the bus, but you can pass an argument into the tool to restrict its search space if necessary.  For example if you know the Device ID is 12345678 you can scan the bus using 12345678FFFFFFFF (where F indicates to libmbus to wildcard that half-byte).

You can see from the output above the secondary addresses of the same three slaves given in the primary address example.

Also worthy of note is that one of my M-Bus slaves appears to have invalid ID data as the Device ID is reported as 99999999 and the manufacturer ID is FFFF.  This is probably as a result of a poor M-Bus software implementation, or a failure to correctly flash this information during manufacture.  (Note, however, that the M-Bus protocol does allow for the Device ID to be configured during operation, so it is possible this slave is intended to have this information configured by the user.)

To retrieve data from the secondary address use mbus-serial-request-data as before, but providing the secondary address instead of the primary:

```
$ mbus-serial-request-data -b 2400 /dev/ttyAMA0 181129145F1D0102
<?xml version="1.0" encoding="ISO-8859-1"?>
<MBusData>

    <SlaveInformation>
        <Id>18112914</Id>
        <Manufacturer>GJ_</Manufacturer>
        <Version>1</Version>
        <ProductName></ProductName>
        <Medium>Electricity</Medium>
        <AccessNumber>85</AccessNumber>
        <Status>00</Status>
        <Signature>0000</Signature>
    </SlaveInformation>

    <DataRecord id="0">
        <Function>Instantaneous value</Function>
        <StorageNumber>0</StorageNumber>
        <Unit>Energy (100 Wh)</Unit>
        <Value>0</Value>
        <Timestamp>2020-04-11T09:39:57Z</Timestamp>
    </DataRecord>

</MBusData>
```

# Changing Addresses

Addresses can normally be changed using two mechanisms:

* Some implemention specific mechanism on the slave - which might be via dip switches or a screen and buttons.

* Using the M-Bus protocol.  The protocol allows for the following to be changed, although note that not all slaves will support all mechanisms:

  * Primary address
  * Secondary address
  * Device ID

libmbus supports changing the primary address using mbus-serial-set-address:

```
$ mbus-serial-set-address -b 2400 /dev/ttyAMA0 2 12
Set primary address of device to 12

$ mbus-serial-scan -b 2400 /dev/ttyAMA0
Found a M-Bus device at address 1
Found a M-Bus device at address 12
Found a M-Bus device at address 48
```

If the slave doesn't support changing the primary address you may see this:

```
mbus-serial-set-address -b 2400 /dev/ttyAMA0 1 11
No reply from device
```

libmbus does not support changing the Device ID or secondary address.
