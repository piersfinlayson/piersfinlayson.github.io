---
layout: post
title:  "Building a custom MicroPython firmware image for the Raspberry Pi Pico W"
date:   2023-09-05 7:01 +0000
tags:   raspberry pi pico bare metal gcc arm python MicroPython
---

This post explains how to build a custom MIcroPython image, with your own main.py script in it, for a Pico W.

## Get and Build MicroPython

Follow the instructions [here](building-micropython-for-pico-w) to install and build MicroPython

## Add your Script and Rebuild

In this example I have a python script /tmp/main.py with these contents:

```
import time
while 1:
  print("tick")
  time.sleep(1)
```

Put it in the ports/rpi/modules directory.  It must be called main.py, as that is what the MicroPython startup code looks for (see ports/rp2/main.c):

```
cp /tmp/main.py ~/builds/MicroPython/ports/rp2/modules/
```

Now build MicroPython (again):

```
cd ~/builds/MicroPython
make -C ports/rp2 -j 4 BOARD=RPI_PICO_W
```

This should be very quick if you've already built MicroPython once, it should just pull in your main.py script and reuild the image:


```
...
make[3]: Entering directory '/home/pdf/builds/MicroPython/ports/rp2/build-RPI_PICO_W'
MPY main.py
GEN /home/pdf/builds/MicroPython/ports/rp2/build-RPI_PICO_W/frozen_content.c
make[3]: Leaving directory '/home/pdf/builds/MicroPython/ports/rp2/build-RPI_PICO_W'
[  6%] Built target BUILD_FROZEN_CONTENT
make[3]: Entering directory '/home/pdf/builds/MicroPython/ports/rp2/build-RPI_PICO_W'
Scanning dependencies of target firmware
make[3]: Leaving directory '/home/pdf/builds/MicroPython/ports/rp2/build-RPI_PICO_W'
make[3]: Entering directory '/home/pdf/builds/MicroPython/ports/rp2/build-RPI_PICO_W'
[  7%] Building C object CMakeFiles/firmware.dir/frozen_content.c.obj
...
```

Check you have a new firmware.uf2:

```
ls -go ports/rp2/build-RPI_PICO_W/firmware.uf2
```

Now shows:

```
-rw-r--r-- 1 1607680 Sep  5 12:28 ports/rp2/build-RPI_PICO_W/firmware.uf2
```

This is 512 bytes larger than the version without our main.py.

## Install and Run

Now install this new image as before:

```
sudo mount /dev/sda1 /mnt
sudo cp ~/builds/MicroPython/ports/rp2/build-RPI_PICO_W/firmware.uf2 /mnt/
sudo umount /mnt/
```

Connect to the USB terminal:

```
minicom -o -D /dev/ttyACM0
```

You should see:
```
tick
tick
tick
...
