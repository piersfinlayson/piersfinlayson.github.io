---
layout: post
title:  "Building Raspberry Pi Pico W examples"
date:   2023-09-05 7:03 +0000
tags:   raspberry pi pico sdk example bare metal
---

This post explains how to build Pico W examples.  It assumes you already have
* the SDK and picotool installed as described [here](installing-pico-sdk-and-picotool)
* the ARM GNU toolchain, which you find instructions for installing [here](building-micropython-for-pico-w).

## Get the examples

```
mkdir -p ~/builds/
cd ~/builds
git clone https://github.com/raspberrypi/pico-examples
```

## Build an example

First of all, we need to get set up the build environment.  If you plan to build and run the WiFi examples, make sure you update YOUR_SSID and YOUR_PASSWORD in the cmake command below.

```
export PICO_SDK_PATH=~/builds/pico-sdk
export PICO_TOOLCHAIN_PATH=~/builds/arm-gnu-toolchain-12.3.rel1-aarch64-arm-none-eabi
cd ~/builds/pico-examples
cmake . -DPICO_BOARD=pico_w -DWIFI_SSID="YOUR_SSID" -DWIFI_PASSWORD="YOUR_PASSWORD"
```

Next choose which example to build.  Note there's not much point trying blinky on the Pico W, as the on-board LED is attached to the WiFI and will not blink via this example.

The examples are in directories.  We're going to build wifi_scan which can be found at ```pico_w/wifi/wifi_scan```.  Before we build, though, we need to modify the project's CMakeLists.txt, because we want serial to work over USB, rather than the default UART:

```
nano ~/builds/pico-examples/pico_w/wifi/wifi_scan/CMakeLists.txt
```

Add this line after the last line of text:

```
pico_enable_stdio_usb(picow_wifi_scan_poll 1)
```

Exit nano (Ctrl-X, then Y then Enter).

Now we need to build the makefiles again:

```
cd ~/builds/pico-examples
cmake .
```

Now we're ready to build the example itself

```
make -j 4 -C ~/builds/pico-examples/pico_w/wifi/wifi_scan
```

We should now have two shiny new uf2 firmware files:

```
ls -go ~/builds/pico-examples/pico_w/wifi/wifi_scan/*.uf2
```

Shows:

```
-rw-r--r-- 1 628736 Sep  5 13:18 /home/pi/builds/pico-examples/pico_w/wifi/wifi_scan/picow_wifi_scan_background.uf2
-rw-r--r-- 1 656896 Sep  5 13:30 /home/pi/builds/pico-examples/pico_w/wifi/wifi_scan/picow_wifi_scan_poll.uf2
```

We get two images, because CMakeLists.txt is configured to create two different versions - one runs in the background (allowing for other work to happen), and the other polls in the foreground.

We'll just use the foreground version for now.  (And we only enabled USB serial for that version.)

## Running the Example

Plug your Pico W into your Raspberry Pi while holding down the Pico's BOOTSEL button and figure out what device it is:


```
sudo dmesg |grep "Attached SCSI removable disk"
```

Will show for example:

```
[12307.427345] sd 0:0:0:0: [sda] Attached SCSI removable disk
```

This Pico W is /dev/sda.  We'll assume that below.  If you didn't see anything you probably failed to hold down BOOTSEL - try unplugging and replugging while holding down the button.

We now mount /dev/sda1, copy the firnmware image over and then unmount:

```
sudo mount /dev/sda1 /mnt && sudo cp ~/builds/pico-examples/pico_w/wifi/wifi_scan/picow_wifi_scan_poll.uf2 /mnt && sudo umount /mnt
```

The firmware should now be running.  We'll connect over a serial terminal and see what we can see:

```
sudo apt -y install minicom
minicom -o -D /dev/ttyACM0
```

You should see output like periodically (obviously unredacted in your case):

```
Performing wifi scan
ssid: Guest-BTWholeHome-XXX            rssi:  -86 chan:   1 mac: 46:fe:3b:xx:xx:xx sec: 5
ssid:                                  rssi:  -83 chan:   1 mac: 46:fe:3b:xx:xx:xx sec: 5
ssid: BTWholeHome-XXX                  rssi:  -91 chan:   1 mac: d4:86:60:xx:xx:xx sec: 5
ssid: playground                       rssi:  -32 chan:   7 mac: d8:3a:dd:xx:xx:xx sec: 5
ssid: playground                       rssi:  -25 chan:   7 mac: d8:3a:dd:xx:xx:xx sec: 5
ssid: playground                       rssi:  -25 chan:   7 mac: d8:3a:dd:xx:xx:xx sec: 5
ssid: BTBHub6-XXXX                     rssi:  -85 chan:   6 mac: 00:cb:51:xx:xx:xx sec: 5
ssid: BTWi-fi                          rssi:  -84 chan:   6 mac: 02:cb:51:xx:xx:xx sec: 0
ssid: playground                       rssi:  -26 chan:   7 mac: d8:3a:dd:xx:xx:xx sec: 5
ssid: playground                       rssi:  -25 chan:   7 mac: d8:3a:dd:xx:xx:xx sec: 5
ssid: playground                       rssi:  -25 chan:   7 mac: d8:3a:dd:xx:xx:xx sec: 5
ssid: playground                       rssi:  -29 chan:   7 mac: d8:3a:dd:xx:xx:xx sec: 5
ssid:                                  rssi:  -89 chan:  11 mac: 7a:d7:aa:xx:xx:xx sec: 5
ssid: SKYXXXXX                         rssi:  -83 chan:  11 mac: 00:a3:88:xx:xx:xx sec: 5
ssid: BT-HRXXXX                        rssi:  -84 chan:  11 mac: c0:d7:aa:xx:xx:xx sec: 5
```

I'm not quite sure why it sees the same networks multiple times - "playground" is an AP running on the host Raspbery Pi (so very close, hence the strong signal strength) .

Use Ctrl-A then X then Enter to exit minicom.
