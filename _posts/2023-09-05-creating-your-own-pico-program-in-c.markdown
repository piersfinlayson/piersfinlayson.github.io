---
layout: post
title:  "Creating your own Pico program using the C SDK"
date:   2023-09-05 7:04 +0000
tags:   raspberry pi pico sdk picotool bare metal
---

This post explains how to create your own C SDK program for the Pico, and assumes you've already [insalled the SDK](installing-pico-sdk-and-picotool).

## Write the code

Create a location for your program:

```
mkdir -p ~/builds/pico-hello-world
cd ~/builds/pico-hello-world
```

Create the program:

```
nano hello-world.c
```

With these contents:

```
#include <stdio.h>
#include <pico/stdlib.h>
#include "pico/binary_info.h"

int main()
{
  bi_decl(bi_program_description("Hello World Program"));
  stdio_init_all();
  while (1)
  {
    puts("Hello World");
    sleep_ms(1000);
  }
}
```

Exit nano (Ctrl-X, then Y then Enter).

Create a CMakeLists.txt file:

```
nano CMakeLists.txt
```

With these contents:

```
cmake_minimum_required(VERSION 3.13)
include(pico_sdk_import.cmake)
project(test_project C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
pico_sdk_init()
add_executable(hello-world
  hello-world.c
)
pico_enable_stdio_usb(hello-world 1)
pico_enable_stdio_uart(hello-world 1)
pico_add_extra_outputs(hello-world)
target_link_libraries(hello-world pico_stdlib)
```

Copy pico_sdk_import.cmake from the SDK directory to this one:

```
export PICO_SDK_PATH=~/builds/pico-sdk
cp $PICO_SDK_PATH/external/pico_sdk_import.cmake .
```

## Building

```
cmake .
make -j 4
```

We should now have a uf2 file:

```
ls -go hello-world.uf2
```

This gives:

```
-rw-r--r-- 1 47104 Sep  5 15:08 hello-world.uf2
```

## Running

This should be familiar by now:

```
sudo mount /dev/sda1 /mnt && sudo cp hello-world.uf2 /mnt && sudo umount /mnt
minicom -o -D /dev/ttyACM0
```

Gives output:
```
Hello World
Hello World
...
```

We can inspect the uf2 file created, using picotool:

```
picotool info -a hello-world.uf2
```

This gives:

```
File hello-world.uf2:

Program Information
 name:          hello-world
 description:   Hello World Program
 features:      UART stdin / stdout
                USB stdin / stdout
 binary start:  0x10000000
 binary end:    0x10005b5c

Fixed Pin Information
 0:  UART0 TX
 1:  UART0 RX

Build Information
 sdk version:       1.5.1
 pico_board:        pico
 boot2_name:        boot2_w25q080
 build date:        Sep  5 2023
 build attributes:  Release
 ```