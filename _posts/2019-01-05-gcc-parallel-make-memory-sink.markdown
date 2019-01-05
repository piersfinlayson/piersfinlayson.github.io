---
layout: post
title:  "Parallel make of gcc is a memory sink"
date:   2019-01-05 10:55:00 +0000
categories: rapsberry pi linux gcc vm virtual memory ram
---

Typically, a few days after [posting]({% post_url 2019-01-02-more-ram-on-a-pi %}) that I couldn't find a way of getting gcc to compile successfully on a Raspberry Pi Zero due to a lack of RAM, I found a solution.

The problem was due to the fact that I was using the same Dockerfile for a 4 core X86-64 machine, a Raspberry Pi 3 (also with 4 cores) and for the lowly single core Pi Zero.  And more importantly, to speed up the builds on the faster machines I was executing make with the parallel make option *-j4*.

This tells make to run up to 4 jobs in parallel during an operation, and that was simply using up too much RAM on the Pi Zero.

When I went back to *-j1* (or in fact not specifying it), the build completed successfully (if turgidly slowly).

Of course, I still want a single Dockerfile for all platforms, so I needed to find a way of running with the appropriate parallel make setting.

It's bit tricky to set up an conditional environment variable with Dockerfile-wide scope in the Dockerfile itself, so as I already have a script which executes the docker build operation to build an appropriately named imaged on each platform, I put the new conditional logic in that script and now pass in the appropriate parallel make option as a --build-arg to docker build as so:

```
ARCH=$(docker info 2> /dev/null|grep Architecture|awk '{print $2}')
if [ $ARCH == armv6l ]
  then
    # Raspberry Pi Zeros only have a single core and not enough RAM to do parallel building of GCC
    PARALLEL_MAKE=
else
  PARALLEL_MAKE="-j4"
fi
docker build --build-arg PARALLEL_MAKE=$PARALLEL_MAKE ...
```

The Dockerfile then accesses it like this:

```
ARG PARALLEL_MAKE
RUN make $PARALLEL_MAKE ...
```

The complete script is [here](https://github.com/piersfinlayson/otbiot-docker/blob/master/build/build-container.sh) and Dockerfile [here](https://github.com/piersfinlayson/otbiot-docker/blob/master/build/Dockerfile).

