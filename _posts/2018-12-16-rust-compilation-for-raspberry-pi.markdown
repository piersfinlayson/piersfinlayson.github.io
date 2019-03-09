---
layout: post
title:  "Rust (and C) Cross Compilation for the Raspberry Pi"
date:   2018-12-16 16:31:00 +0000
categories: docker containers raspberry pi rust cross compile compilation
---

# Introduction

I've been playing around with the [Rust](https://www.rust-lang.org/) programming language recently.  I'm aiming to run a bunch of Rust-based microservices in minimal docker containers on low cost systems, likely to be primarily ARM based.

One of Rust's selling points is its "top-notch tooling", with built-in cross compilation support, so I thought this would be a breeze.  It look quite a lot more effort than planned though, read on for why.

*Update: 5 January 2019*

I now have a combined x86_64, ARMv7 and ARMv7 build container, available [here](https://hub.docker.com/r/piersfinlayson/build).  Version 0.2.2 onwards.

# Build Container

These days I do all of my developing in containers, to avoid constantly fighting with out of date dependencies, old version of tools, legacy rubbish lying around from previously playing around with different toolsets, etc.  I've now updated my primary build container to support Rust (and C/C++) cross compilation to a couple of different ARM platforms, suitable for all generations of Raspberry Pis, and vice versa (were I enough of a masochist to want to compile anything on a Raspberry Pi!).

The x86_64, ARMv7 and ARMv6 container can be found [here](https://hub.docker.com/r/piersfinlayson/build).  You need at least version 0.2.2 to support all hosts and targets.

The container also provides OpenSSL (for example, if you are building an HTTPS enabled web server), and MUSL libc.

# MUSL libc

MUSL is important is you want a minimal container, with no extra stuff required other than your binary.  A truly minimal container's Dockerfile looks something like this:

```
FROM scratch
COPY my_binary /
CMD ["/my_binary"]
```

However, if you try this with a standard binary you'll get an error like this when you run the container:

```
standard_init_linux.go:178: exec user process caused "no such file or directory"
```

This is because the (GNU) libc.so that the binary was dynamically linked with can't be found on the system, as the container just has the one file in the filesystem (apart from special stuff like /proc/* /dev/* etc).  The error isn't super useful, but indicates the lack of a file needed to run "my_binary".

The way around this is to statically link with a libc - and MUSL libc can be used for this.  To hide a lot of the detail you need 3 things to do this:
* A special version of the compiler and linker on your platform
* The MUSL libc
* A toolchain which can handle using them

The Rust toolchain comes with the second and third items - you just need to bring the first.  If you want to use other third party libraries in your binary then in all likelihood they use libc as well, so you'll need to build them with MUSL libc too.  Hence the reason my build container contains OpenSSL, built for all of x86_64, ARMv7 and ARMv6 - as any supplied OpenSSL version would be linked with GNU libc.

# ARMv6 vs ARMv7

Raspberry Pis use processors from different ARM architecture versions:
* The original Pis and Zero/W are based on ARMv6.
* Later Pis (like the 3) are ARMv7.

The ARMv7 supports more instructions, which aren't supported by ARMv6, making the processor more efficient.  For example the ARMv7 have more hardware floating point instructions than ARMv6.

If you try and run a program built for ARMv7 on ARMv6 you'll likely get an illegal instruction error killing your program (at some point, maybe not immediately, but when an illegal instruction is attempted to be executed).  So if you want to support both types of Pi using a language compiled down to machine code you have two choices:

* Build for the lowest common denominator.  ARMv7 is backwards compatible with ARMv6, so if you build for ARMv6 it will (probably) run on ARMv7.  (Probably because there's a lot of optional instructions in both architectures - I could imagine you could find an ARMv7 based processor which failed to support one or more ARMv6 optional instructions if you tried hard enough.)  The downside of this is that you'll fail to utilise instructions on ARMv7 which might speed up execution.

* Build two binaries, one for each.

# Cross Compilers

If you want to build on a single platform (host) for all of x86_64, ARMv6 and ARMv7 (targets) then you need 3 different cross compilers, and that's just to handle GNU libc.  For MUSL you need another three.

Well, nearly.  You could get away with a single version of the cross compiler handling both ARMv6 and ARMv7 targets - as you can specify dynamically which platform to compile for through compiler flags.

If you're running on an x86_64 host and install a standard gcc package you'll get the ability to compile for that (x86_64) target.  If you install the gcc-arm-linux-gnueabihf package this will give you a version of gcc which will cross compile to both ARmv6 and ARMv7.

To support compiling for a MUSL libc x86_64 target you can use the musl-dev package in ubuntu - which will give you a version of gcc which will compile for x86_64 targets only.  If you want a version to cross compile for MUSL ARMv6/v7 you'll probably need to build your own.

# Building MUSL Cross Compiler

Thankfully people have already taken the complexity out of this - I used the [musl-cross-make](https://github.com/richfelker/musl-cross-make) project, which is pretty simple to use.  Build a config file (config.mak) like this:

```
TARGET=arm-linux-musleabihf
OUTPUT=/opt/cross/armv6
COMMON_CONFIG += CFLAGS="-g0 -Os" CXXFLAGS="-g0 -Os" LDFLAGS="-s"
GCC_CONFIG += --with-arch=armv6 --with-mode=arm --with-fpu=vfp
```

And then run 

```
make install
```

This will instruct the project to build a compiler for use by the current host, to build for an ARMv6 target, and will generate a MUSL libc.  Importantly gcc will be built to compile for:
* ARMv6
* Using VFPv2 hard floating point instructions

Why?  Read on.

# Variants of ARMv6 and ARMv7

This is where is gets a bit more complicated.  As indicated above, even within differnet ARM architecture versions, different processors support different sets of instructions.  I talked about hardware (hard) floating point above.  Many ARMv6 processors including the BCM2835 used in the Pi Zero, support the ARM VFPv2 (also called just VFP) instruction set for floating point support.  However, others don't.  And even if your processor supports VFPv2 your OS (linux kernel) may not, or may not enable its use for userland processes!  (Raspbian does.  I've seen rumours that some versions of armbian don't.)

So, when figuring out how to cross-compile and what your target is you need to know a bit about your hardware and OS.  It's not just the gcc configuration and compiler flags that get changed - the actual target name can change too.  See the target specified above:

```
TARGET=arm-linux-musleabihf
```

Breaking this down it means:
* arm - ARMv6 architecture (other variants of ARM are indicated like armv5 and armv7, but just arm is used for V6)
* linux - the OS
* musleabihf - breaks down further into:
  * musl - MUSL libc
  * eabi - see [here](https://wiki.debian.org/ArmEabiPort)
  * hf - means hard(ware) float(ing point support)

So you'll also see targets such as:
arm-linux-gnueabihf
arm-linux-musleabihf
armv7-linux-gnueabihf
armv7-linux-musleabihf
arm-linux-gnueabi
arm-linux-musleabi

Phew!

# Raspberry Pi Targets

For the Raspberry Pi you may want/need all of:

* arm-linux-gnueabihf
* arm-linux-musleabihf
* armv7-linux-gnueabihf
* armv7-linux-musleabihf

# Rust Targets

Rust target types are similar to those above but also add a vendor part - after the architecture and before the OS.  This is normally left to default (unknown).  So in rust the above Pi targets become:

* arm-unknown-linux-gnueabihf
* arm-unknown-linux-musleabihf
* armv7-unknown-linux-gnueabihf
* armv7-unknown-linux-musleabihf

# Rust Cross Compiling

I won't bother repeating the instructions on Rust compilation give at [this](https://github.com/japaric/rust-cross) excellent project.  Once you have the correct cross compiler installed you can go ahead and follow those.

Or, just use the build container linked to above :-).  Then you can build for any of the following targets just by executing:

```
cargo build --target <TRIPLE>
```

Where TRIPLE is one of the quadruple (!):

* x86_64-unknown-linux-gnu
* x86_64-unknown-linux-musl
* arm-unknown-linux-gnueabihf
* arm-unknown-linux-musleabihf
* armv7-unknown-linux-gnueabihf
* armv7-unknown-linux-musleabihf

Of course Rust supports more targets than this (and you can add your own), but they're outside of the scope of this post.

# Rust ARMv6 Cross Compliation bug

While playing around with this I found a [nasty bug](https://github.com/rust-lang/rust/issues/50583) in Rust's ARMv6 MUSL support.  Actually, I think it's a bug in gcc, but gets exposed because Rust builds MUSL libc built without specifying the -mfpu=vfp flag shown above, which leads gcc to (erroneously I believe) add in VFPv3 instructions (which ARMv6 doesn't support).  This version of libc is statically linked into liblibc which rustup uses to then link into your MUSL ARMv6 binary.  Which then causes the binary to barf with an illegal instruction error when executed.

This bug is the reason I now far more about Rust toolchains and cross compilers than I ever thought I would - as cross compilation for the ARMv6 target didn't just work.

The main Rust codebase has now been [patched](https://github.com/rust-lang/rust/commit/b17a3f21c239648141e749d5a4b5af4ae0430c2a#diff-bf0d5b0898f46200942e39ec93d84e7c), but as of today that fix isn't in the released version of Rust - hopefully it will be as of 1.32 (January 2019?).  Once that's done I'm hoping - at least for my targets - this _will_ just work!

*Update: 9 March 2019*

I have confirmed this bug is now fixed, as of Rust 1.33.

# Want to Know More?

See the Dockerfile and script which build the container variants referenced above [here](https://github.com/piersfinlayson/otbiot-docker/tree/master/build).

# Update - GNU vs MUSL

Here's the output from ldd from a Rust release binary for a HTTP microservice built using the x86_64 gnu target:

```
        linux-vdso.so.1 (0x00007ffcbd5f3000)
        libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007f123ade8000)
        librt.so.1 => /lib/x86_64-linux-gnu/librt.so.1 (0x00007f123abe0000)
        libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007f123a9c1000)
        libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007f123a7a9000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f123a3b8000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f123b8c9000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007f123a01a000)
```

If you don't have this stuff in your container (and these dependencies may have their own) then your binary won't run.

Here's the output from an x86_64 musl target to contrast:

```
        not a dynamic executable
```

:-)