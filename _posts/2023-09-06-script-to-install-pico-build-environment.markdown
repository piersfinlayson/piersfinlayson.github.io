---
layout: post
title:  "Script and Dockerfile to create Pico build environment"
date:   2023-09-05 7:02 +0000
tags:   raspberry pi pico sdk picotool bare metal docker dockerfile container
---

# pico-build

[This repo](https://github.com/piersfinlayson/pico-build) contains a script and Dockerfile to create a build enviroment for Raspberry Pi Pico and Pico W C and Python development.

It supports Pi (both 32-bit and 64-bit) and x86_64 hosts.

Either use it to install the GNU ARM toolchain and various required (and some useful) packages and repos directly, or use the Dockerfile to create a container image, to use that for development.

## Direct Install

To install directly:

```
./install-pico-build.sh <install-dir> # install-dir is where you want everything installed, such as ~/builds
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