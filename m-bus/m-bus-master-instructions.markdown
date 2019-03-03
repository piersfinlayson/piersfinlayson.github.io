---
layout: post
title: M-Bus Master Hat Instructions
permalink: /m-bus/master/instructions
categories: m-bus mbus raspberry pi master hat instructions manual getting started
exclude: yes
---

<style>
.aligncenter {
    text-align: center;
}
</style>

# Installation

The following picture shows the M-Bus Master Hat mounted on a Raspberry Pi Model 3 A+.  To mount the hat:

<p class="aligncenter">
  <img alt="M-Bus Master Hat mounted on a Raspberry Pi Model 3 A+" src="/static/img/mbus_master_and_pi.JPG" width="360" />
</p>

* First fit the supplied standoffs to the Raspberry Pi.

* Then carefully slide the Hat down the standoffs and mate the 40-pin female connector on the Hat with the male connector on the Pi.

* Once you're sure the connectors are aligned press the Hat firmly onto the Pi so the pins make a good connection.

* Finally use the 4 nuts provided to secure the Hat to the standoffs.

Be careful throughout the process not to damage any components on either the Pi or the Hat.  In particular, avoid the Pi's SD card area - it is easy to snap an SD card by putting too much pressure on it.

# Removal

Removal is the opposite of installation.  The Hat can be very firmly held to the Pi by the connectors and standoffs.  Be careful when sliding the Hat off not to damage any components or bend any pins.  In particular avoid holding the Pi anywhere near the SD card to avoid damaging the SD card or the Pi.

# Power On

Power on the Pi as usual.  The Hat's green "PI" LED should be illuminated.  (Depending the revision of your M-Bus Master the "BUS" LED may be faintly illuminated.)

If using Raspbian the Pi should automatically detect the the Hat at boot.  To confirm this from a terminal session run:
```
cat /proc/device-tree/hat/product
```

You should see:
```
M-Bus Master
```

All further instructions below assume you are using [Raspbian](https://raspbian.org/).

# Enabling Serial Access

The Pi communicates with the M-Bus Master Hat using the serial port.  This requires some configuration on the Pi.

From a terminal run:
```
sudo raspi-config
```

Select
```
Interfacing Options
```

Then
```
Serial
```

Answer
```
Would you like a login shell to be accessible over serial?
=> <No>
```

Answer
```
Would you like the serial port hardware to be enabled?
=> <No>
```

Now select
```
=> <Ok>
=> <Finish>
```

Do not reboot the Pi yet.  If you have a Bluetooth-capable Raspberry Pi you need to reconfigure the Bluetooth port to avoid it using the serial port that will be used by the M-Bus Master Hat.  To do this, edit /boot/config.txt with your favourite text editor.  For example:
```
sudo nano /boot/config.txt
```

At the end of that file add the line:
```
dtoverlay=pi3-miniuart-bt
```

Save /boot/config.txt and then reboot:
```
sudo reboot now
```

Serial device /dev/ttyAMA0 will now be connected to the M-Bus Master Hat.  This is the PL011 UART on the Pi's Broadcom CPU.  See [this post]({% post_url 2019-02-18-raspberry-pi-serial-ports %}) for more information about the Raspberry Pi Serial ports.

# Enable M-Bus

By default the M-Bus will be disabled - there will be no power on the bus.  Before communicating on the bus you need to power the bus on.  If you don't have wiringPi installed, install it now:
```
sudo apt install wiringpi
```

To enable the M-Bus you need to make GPIO 26 high.  WiringPi (confusingly) calls this GPIO 25, so run:
```
gpio write 25 1
```

The Hat's "BUS" LED should now be illuminated brightly.  This confirms bus power is present.  Depending on the revision of your M-Bus Master Hat, the "BUS" LED may glow faintly when there is no bus power present.

To disable the M-Bus again run:
```
gpio write 25 0
```

After a reboot the bus power will automatically be off by default.

# Connecting Slaves

Slaves or a bus of slaves can be connected to the M-Bus Master Hat using the labelled M-Bus +/- connectors.  It doesn't matter which way around you connect the bus/slave cables.  Note that the M-Bus Master Hat is only rated for connection to up to 3 slave devices simultaneously and up to 100m cable runs.

# Using libmbus

No software is provided with the M-Bus Master Hat, but you can use the open source [libmbus](https://github.com/rscada/libmbus) to drive it.

To install libmbus, from a terminal run:
```
sudo apt install git install libtool autoconf
git clone https://github.com/rscada/libmbus
cd libmbus
./build.sh
sudo make install
```

A number of utilities are provided with libmbus - see the [documentation](https://github.com/rscada/libmbus/blob/master/bin/libmbus.pod) for more details.

Once you have connected the M-Bus to the M-Bus Master Hat, a good first step is to scan the bus for connected devices.  Note that while the default M-Bus speed is 2400 baud, your device may have a different baud rate configured - so experiment with different speed settings if you don't immediately find your device.
```
bin/mbus-serial-scan -b 2400 /dev/ttyAMA0
```

You should see output like this (with your slave's address likely being different):
```
Found a M-Bus device at address 48
```

Now you know your M-Bus slave's address, you can query its data:

```
bin/mbus-serial-request-data -b 2400 /dev/ttyAMA0 48
```

The output from this command will the data your slave provided, encoded as XML.  The precise data and format will depend upon the slave type.  See example output [here]({% post_url 2019-03-02-atlas-ec-20-mbus-flow-meter %}).

If you get an error message when running libmbus commands like this:
```
/home/pi/libmbus/bin/.libs/lt-mbus-serial-request-data: error while loading
shared libraries: libmbus.so.0: cannot open shared object file: No such file
or directory
```

Run
```
export LD_LIBRARY_PATH=/usr/local/lib
```

Then try running the command again.

# Problems

If you have any problems with your M-Bus Master Hat, please [contact me](mailto:mbus@packom.net) with details of your problem.

Please note that I do not provide support for libmbus, but will provide best effort assistance if you are having trouble to get it to work with your M-Bus Master Hat.
