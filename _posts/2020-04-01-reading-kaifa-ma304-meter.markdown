---
layout: post
title:  "Reading a Kaifa MA304 Electricity Meter using a Raspberry Pi"
date:   2020-04-01 9:00 +0000
tags:   pi mbus m-bus obis dlms kaifa ma304 power energy hat master serial dlms cosem iec 62056
---

Many properties in Norway and Sweden have had Kaifa MA304 smart meters rolled out to them in recent years.  Here's how to use a Raspberry Pi to read it remotely.

You will need:
* An M-Bus Master like the [M-Bus Master Hat](https://www.packom.net/m-bus-master-hat/).
* The [AMS Han Decoder](https://github.com/packom/ams-han-decoder) software.
* A Raspberry Pi (any model with a 40 pin GPIO header will do).
* An ethernet cable (CAT-5 is fine).

Follow these instructions at your own risk, and in particular steer clear of any mains voltage cables!

## Instructions

# Installing the M-Bus Master

Connect the M-Bus Master to your Pi.  To use the M-Bus Master Hat follow the following sections from the instructions [here](https://www.packom.net/m-bus-master-hat-instructions/):
* Installation
* Powering On
* Enabling Serial Access
* Enable M-Bus

You will need to repeat the "Enable M-Bus" instructions after a reboot of the Pi to enable the M-Bus power:

```
gpio write 25 1
```

If red LED of the M-Bus Master Hat is lit you're ready to continue.

# Connect to your Kaifa M-Bus Meter

Take your ethernet cable and cut one of the ends off.

Strip the white/brown and brown cables and insert into your M-Bus Master - either way around is fine.  Take care to use the correct colours - these should be connected to pins 7 & 8 of the remaining RJ-45 plug.

Connect the remaining RJ-45 plug into your Kaifa MA304 meter's RJ-45 socket - you may have to lift a flap labelled M-Bus to access the socket.

# Install Software to Read the Meter

Tun these commands on your Pi (installed with Raspbian):

```
sudo apt install libjson-perl
sudo apt install libdigest-crc-perl
wget https://raw.githubusercontent.com/packom/ams-han-decoder/master/ams_han_decoder.pl
chmod +x ams_han_decoder.pl
```

# Read the Meter

If using the M-Bus Master Hat make sure the red LED is lit:

```
gpio write 25 1
```

Then run:

```
./ams_han_decoder.pl -m KFM_001 /dev/ttyAMA0
```

The Kaifa MA304 reports:

* The active (instantaneous) power every 2 seconds

* Much more comprehensive (instantaneous) information every 10 seconds

* Cumulative power usage information every hour, in addition to the 10s information

# Sample Output

The software was tested on a Kaifa MA304H4D, and provided the following output:

```
{
   "data" : {
      "energy_active_cum_export" : {
         "description" : "Cumulative hourly active export energy (A-) (Q2+Q3)",
         "obis_code" : "1-0:2.8.0.255",
         "unit" : "kWh",
         "value" : 2853.145
      },
      "energy_active_cum_import" : {
         "description" : "Cumulative hourly active import energy (A+) (Q1+Q4)",
         "obis_code" : "1-0:1.8.0.255",
         "unit" : "kWh",
         "value" : 11589.514
      },
      "energy_reactive_cum_export" : {
         "description" : "Cumulative hourly reactive export energy (R-) (Q3+Q4)",
         "obis_code" : "1-0:4.8.0.255",
         "unit" : "kVArh",
         "value" : 4285.508
      },
      "energy_reactive_cum_import" : {
         "description" : "Cumulative hourly reactive import energy (R+) (Q1+Q2)",
         "obis_code" : "1-0:3.8.0.255",
         "unit" : "kVArh",
         "value" : 120.588
      },
      "meter_id" : {
         "description" : "Meter ID (GIAI GS1)",
         "obis_code" : "0-0:96.1.0.255",
         "value" : "!!!!REDACTED!!!!"
      },
      "meter_timestamp" : {
         "description" : "Meter timestamp",
         "obis_code" : "0-0:1.0.0.255",
         "value" : "2020-04-02 12:39:00,255 -32768 (0)"
      },
      "meter_type" : {
         "description" : "Meter type",
         "obis_code" : "0-0:96.1.7.255",
         "value" : "MA304H4D"
      },
      "obis_version" : {
         "description" : "OBIS list version identifier",
         "obis_code" : "1-1:0.2.129.255",
         "value" : "KFM_001"
      },
      "phase_current_l1" : {
         "description" : "IL1 Current phase L1",
         "obis_code" : "1-0:31.7.0.255",
         "unit" : "A",
         "value" : 1.661
      },
      "phase_current_l2" : {
         "description" : "IL2 Current phase L2",
         "obis_code" : "1-0:51.7.0.255",
         "unit" : "A",
         "value" : 2.103
      },
      "phase_current_l3" : {
         "description" : "IL3 Current phase L3",
         "obis_code" : "1-0:71.7.0.255",
         "unit" : "A",
         "value" : 1.337
      },
      "phase_voltage_l1" : {
         "description" : "UL1 Phase voltage 4W meter, line voltage 3W meter",
         "obis_code" : "1-0:32.7.0.255",
         "unit" : "V",
         "value" : 228.9
      },
      "phase_voltage_l2" : {
         "description" : "UL2 Phase voltage 4W meter, line voltage 3W meter",
         "obis_code" : "1-0:52.7.0.255",
         "unit" : "V",
         "value" : 228.8
      },
      "phase_voltage_l3" : {
         "description" : "UL3 Phase voltage 4W meter, line voltage 3W meter",
         "obis_code" : "1-0:72.7.0.255",
         "unit" : "V",
         "value" : 227.7
      },
      "power_active_export" : {
         "description" : "Active power export (Q2+Q3)",
         "obis_code" : "1-0:2.7.0.255",
         "unit" : "W",
         "value" : 721
      },
      "power_active_import" : {
         "description" : "Active power import (Q1+Q4)",
         "obis_code" : "1-0:1.7.0.255",
         "unit" : "W",
         "value" : 0
      },
      "power_reactive_export" : {
         "description" : "Reactive power export (Q3+Q4)",
         "obis_code" : "1-0:4.7.0.255",
         "unit" : "VAr",
         "value" : 195
      },
      "power_reactive_import" : {
         "description" : "Reactive power import (Q1+Q2)",
         "obis_code" : "1-0:3.7.0.255",
         "unit" : "VAr",
         "value" : 0
      }
   },
   "header" : {
      "apdu_invoke_id_and_priority" : "40000000",
      "apdu_tag" : "0f",
      "hdlc_addr_client" : "01",
      "hdlc_addr_server" : "0001",
      "hdlc_control" : "10",
      "hdlc_fcs" : "4f07",
      "hdlc_frame_format" : "a09b",
      "hdlc_hcs" : "561b",
      "hdlc_length" : 155,
      "hdlc_segmentation" : 1,
      "hdlc_type" : 11,
      "llc_control" : "00",
      "llc_dst_svc_ap" : "e6",
      "llc_src_svc_ap" : "e7"
   },
   "payload" : [
      "\u0007ä\u0004\u0002\u0004\f'\u0000ÿ�\u0000\u0000",
      [
         "KFM_001",
         "!!!!REDACTED!!!!",
         "MA304H4D",
         0,
         721,
         0,
         195,
         1661,
         2103,
         1337,
         2289,
         2288,
         2277,
         "\u0007ä\u0004\u0002\u0004\f'\u0000ÿ�\u0000\u0000",
         11589514,
         2853145,
         120588,
         4285508
      ]
   ]
}
```

# Technical Details

At first glance the Kaifa MA304 claims to support [M-Bus](https://m-bus.com/documentation).  In fact it only support the M-Bus [physical layer](https://m-bus.com/documentation-wired/04-physical-layer), master-slave architecture, with a nominal +36V bus, and uses voltage drops to signal from the master to slave, and current draws to communicate from the slave to the master.

For protocol communication the Kaifa MA304 supports the [DLMS/COSEM](https://www.dlms.com/dlms-cosem/overview) standard instead of the M-Bus [data link](https://m-bus.com/documentation-wired/05-data-link-layer), [application](https://m-bus.com/documentation-wired/06-application-layer) and [network](https://m-bus.com/documentation-wired/07-network-layer) layers, over the top of the M-Bus physical layer.  This is a standard serial protocol running at 2400,8,N,1 with information encoded according to the DLMS/COSEM specs and OBIS objects (IEC 62056).

The Kaifa MA304 reports serial data when the M-Bus port is powered every 2 seconds, with additional data every 10s and hour.  For more details see [this document](/static/files/S1001_Kaifa.HAN.OBIS.codes.KFM_001.pdf).  The wiring diagram for the Kaifa MA304 M-Bus/OBIS port is [here](/static/img/ma304_wiring.png).
