---
layout: post
title:  "Single install script and/or container for Pico development"
date:   2023-09-07 6:59 +0000
tags:   raspberry pi pico sdk picotool bare metal docker dockerfile container build
---

[This repo](https://github.com/piersfinlayson/pico-build) contains a script and Dockerfile to create a build enviroment for Raspberry Pi Pico and Pico W C and Python development.

It supports Pi (both 32-bit and 64-bit) and x86_64 hosts.

Either use it to install the GNU ARM toolchain and various required (and some useful) packages and repos directly, or use the Dockerfile to create a container image, to use that for development.

## Direct Install

To install directly:

```
./install-pico-build.sh <install-dir> # install-dir is where you want everything installed, such as ~/builds
```

The pico-sdk is located at:

```
<install-dir>/pico-sdk
```

The ARM GNU toolchain is:

```
<install-dir>/arm-gnu-toolchain
```

Both PICO_SDK_PATH and PICO_TOOLCHAIN_PATH are set up in .bashrc by this script, but if you need to export manually:

```
export PICO_SDK_PATH=<install-dir>/pico-sdk
export PICO_TOOLCHAIN_PATH=<install-dir>/arm-gnu-toolchain
```

## Container Image

To create a container image:

```
docker build . -t pico-build
```

To run the container, use a command like:

```
docker run --rm -ti pico-build
```
