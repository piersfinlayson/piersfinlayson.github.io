---
layout: post
title:  "Driving the M-Bus Master Hat using Python - pyMbusHat"
date:   2020-01-18 9:00 +0000
tags:   pi mbus m-bus power energy hat pyMeterBus pyMbusHat
---

I've already posted about driving the Raspberry Pi [M-Bus Master Hat](https://www.packom.net/m-bus-master-hat/) I developed via [HTTP](https://piers.rocks/m-bus/mbus/rpi/raspberry/pi/restful/microservice/2019/03/16/mbus-httpd.html) and you can also use the command line using [libmbus](https://www.packom.net/m-bus-master-hat-instructions/#using-libmbus).

Another option is [python](https://www.python.org/), using the [pyMeterBus](https://github.com/ganehag/pyMeterBus) project.

I've written a sample app [pyMbusHat](https://github.com/packom/pyMbusHat) which checks a Hat is installed, powers the M-Bus up, and uses pyMeterBus to communicate with M-Bus slaves.

Here's some sample output from reading an ATS water meter:
```
Found M-Bus Master Hat version 0x0005
{
    "body": {
        "header": {
            "access_no": 112,
            "identification": "0x30, 0x13, 0x73, 0x15",
            "manufacturer": "ATS",
            "medium": "0x4",
            "sign": "0x0, 0x0",
            "status": "0x0",
            "type": "0x72",
            "version": "0x1"
        },
        "records": [
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "type": "VIFUnit.ENERGY_WH",
                "unit": "MeasureUnit.WH",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "type": "VIFUnit.VOLUME",
                "unit": "MeasureUnit.M3",
                "value": 0.05000000000000000277555756156289135105907917022705078125
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "type": "VIFUnit.ON_TIME",
                "unit": "MeasureUnit.SECONDS",
                "value": 138085200
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "type": "VIFUnit.POWER_W",
                "unit": "MeasureUnit.W",
                "value": 1000
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "type": "VIFUnit.VOLUME_FLOW",
                "unit": "MeasureUnit.M3_H",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "type": "VIFUnit.FLOW_TEMPERATURE",
                "unit": "MeasureUnit.C",
                "value": 0.01000000000000000020816681711721685132943093776702880859375
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "type": "VIFUnit.RETURN_TEMPERATURE",
                "unit": "MeasureUnit.C",
                "value": 0.01000000000000000020816681711721685132943093776702880859375
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "type": "VIFUnit.TEMPERATURE_DIFFERENCE",
                "unit": "MeasureUnit.K",
                "value": 0.01000000000000000020816681711721685132943093776702880859375
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "type": "VIFUnit.DATE",
                "unit": "MeasureUnit.DATE",
                "value": "2020-01-15"
            }
        ]
    },
    "head": {
        "a": "0x30",
        "c": "0x8",
        "crc": "0xdd",
        "length": "0x3d",
        "start": "0x68",
        "stop": "0x16"
    }
}
```

And here's some less exciting  output from reading an SDM220-MBUS electricity meter:

```
Found M-Bus Master Hat version 0x0005
{
    "body": {
        "header": {
            "access_no": 85,
            "identification": "0x99, 0x99, 0x99, 0x99",
            "manufacturer": "___",
            "medium": "0x2",
            "sign": "0x0, 0x0",
            "status": "0x0",
            "type": "0x72",
            "version": "0x1"
        },
        "records": [
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "type": "VIFUnit.ENERGY_WH",
                "unit": "MeasureUnit.WH",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "type": "VIFUnit.ENERGY_WH",
                "unit": "MeasureUnit.WH",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "type": "VIFUnit.ENERGY_WH",
                "unit": "MeasureUnit.WH",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "type": "VIFUnit.ENERGY_WH",
                "unit": "MeasureUnit.WH",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "type": "VIFUnit.ENERGY_WH",
                "unit": "MeasureUnit.WH",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "type": "VIFUnit.ENERGY_WH",
                "unit": "MeasureUnit.WH",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "type": "VIFUnitExt.DIMENSIONLESS",
                "unit": "MeasureUnit.NONE",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "type": "VIFUnitExt.DIMENSIONLESS",
                "unit": "MeasureUnit.NONE",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "type": "VIFUnitExt.DIMENSIONLESS",
                "unit": "MeasureUnit.NONE",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "type": "VIFUnitExt.DIMENSIONLESS",
                "unit": "MeasureUnit.NONE",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "type": "VIFUnitExt.DIMENSIONLESS",
                "unit": "MeasureUnit.NONE",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "type": "VIFUnitExt.DIMENSIONLESS",
                "unit": "MeasureUnit.NONE",
                "value": 0
            }
        ]
    },
    "head": {
        "a": "0x1",
        "c": "0x8",
        "crc": "0x27",
        "length": "0x5d",
        "start": "0x68",
        "stop": "0x16"
    }
}
```
