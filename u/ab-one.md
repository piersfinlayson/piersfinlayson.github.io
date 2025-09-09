---
layout: default
title: Adrian Black - One ROM
---
Hi Adrian,

<img src="https://raw.githubusercontent.com/piersfinlayson/one-rom/main/docs/images/one-rom-24-pin-rp2350-rev-a-side.png" alt="One ROM" width="40%" style="float: right;">

Here are some notes on the One ROMs I gave you are VCF Midwest, to help get you started.

[https://piers.rocks/u/one](https://piers.rocks/u/one)

As a reminder One ROM used to be called Software Defined Retro ROM and aims to be the most flexible ROM replacement for retro systems, with a single hardware PCB supporting all 2316/2332/2364 mask programmed variants - that's 14 different chip select options.

One ROM's firmware and hardware are fully open source.

For a quick description of One ROM's main features see [Key Features](https://github.com/piersfinlayson/one-rom/tree/main/README.md#key-features).

For instructions on programming ROMs, selecting images, and other common tasks, see [Getting Started](https://github.com/piersfinlayson/one-rom/tree/main/docs/GETTING-STARTED.md).

I gave you 4 ROMs, each with a different pre-installed ROM collection:

- **G 411** - A collection of stock C64 KERNAL/BASIC/Character/Dead Test ROMs.  See [the config](https://github.com/piersfinlayson/one-rom/tree/main/config/c64-no-destestmax.mk) for details.  Just stick this One ROM in a C64 as the kernal and it should work straight away.  Use the [image select jumpers](https://github.com/piersfinlayson/one-rom/tree/main/docs/GETTING-STARTED.md#image-selection) to select BASIC/Character/Dead Test ROMs.

- **F 405** - A collection of different C64 character ROMs.  See [the config](https://github.com/piersfinlayson/one-rom/tree/main/config/bank-c64-char-fun.mk) for details.  Again, just replace a C64's stock character ROM and it should work straight away.  Use the [bank select jumpers](https://github.com/piersfinlayson/one-rom/tree/main/docs/GETTING-STARTED.md#bank-selection) to select different character ROMs on the fly.

- **F 446** - A collection of stock VIC-20 NTSC KERNAL/BASIC/Character/Dead Test ROMs.  See [the config](https://github.com/piersfinlayson/one-rom/tree/main/config/vic20-ntsc.mk) for details.

- **R** - A (very new) Raspberry Pi RP2350 based One ROM, with a multi-ROM set for the C64 including KERNAL/BASIC/Character ROM.  This single One ROM replaces all three ROMs simultaneously.  See [the config](https://github.com/piersfinlayson/one-rom/tree/main/config/set-c64.mk) and [Multi-ROM Sets](https://github.com/piersfinlayson/one-rom/tree/main/docs/GETTING-STARTED.md#multi-rom-sets) for details.

The 411/405/446 above indicate the type of STM32F4 MCU used on that One ROM.  F/G indicate different PCB revisions.

Different STM32 MCUs can run at different max clock speeds, and have different flash sizes.  The F405/F446 are most suitable for machines **faster** than the C64 as they can be clocked the fastest.  Pretty much all features are available on both STM32 and RP2350 MCUs.

Because this is a software solution, and true to One ROM's aim to be the most flexible ROM replacement, there's lots of [configuration options](https://github.com/piersfinlayson/one-rom/tree/main/docs/CONFIGURATION.md) available, including MCU custom clock speeds, overclocking, configurable status LED, supporting custom third-party PCB layouts, automatically replicating smaller ROM images to server as larger ROM sizes, logging, etc.  I've even used One ROM to instrument a running C64's ROM access patterns, over WiFi, with [Airfrog](https://github.com/piersfinlayson/airfrog/blob/main/README.md#example-use-case---remote-telemetry).

As well as [One ROM Lab](https://github.com/piersfinlayson/one-rom/tree/main/rust/lab/README.md) which reads other ROMs, I'm also working on a One ROM USB variant which will be easier to program, and a 28-pin version.

Have fun and do reach out if you have any questions or problems.

Piers
