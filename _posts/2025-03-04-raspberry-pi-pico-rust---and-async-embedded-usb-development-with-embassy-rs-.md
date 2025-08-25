---
layout: post
title: "Raspberry Pi Pico Rust 🦀 and async embedded USB development with embassy-rs."
date: 2025-03-04
categories: youtube
youtube_id: LtJW3SM8i-A
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/LtJW3SM8i-A" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

Learn how to implement a vendor-specific USB device in Rust with ease.  

In this episode I use Rust to develop an embedded USB vendor device on the Pico.  This uses Rust's async and futures support, and provides a simple but complete example implementing control and bulk transfers, following a subset of the protocol used by the xum1541 project (part of OpenCBM).  

My previous video covered a functionally identical example in C using the TinyUSB Stack and Pico SDK. It is here: <https://www.youtube.com/watch?v=f_c9s5aC1No>  

This tutorial covers:  
- Setting up a basic USB vendor device  
- Implementing USB descriptors  
- Handling static lifetimes  
- Handling control and bulk transfers  
- Using embassy's task executor  
- A watchdog timer  
- Mutexes  
- Comparisons between the TinyUSB stack and embassy  
- Lots of other stuff!  

As well as the Pico (Rp2040 and RP2350) embassy supports the ESP32, STM32 and Nordic devices.  


### Timestamps

00:00 Intro  
02:37 Building, flashing and running  
05:00 Modules  
05:50 USB Descriptor and other setup  
14:04 Control handling  
20:52 Bulk handling  
25:40 Protocol handling  
29:49 Constants  
30:32 Conclusions and wrap-up  

The complete source code and documentation is available at:  
<https://github.com/piersfinlayson/embassy-usb-vendor-example>  

This example is perfect for anyone wanting to:  
- Learn USB device development with Rust  
- Create custom USB peripherals with Rust  
- Understand low-level USB communication  
- Get started with the Raspberry Pi Pico with  Rust  

Prerequisites:  
- Basic familiarity with Rust programming  
- 2 x Raspberry Pi Picos (one for use as a debug probe)  
- Development environment set up for Rust - although full instructions for building and flashing the example are in the project.  

If you found this useful and interesting, please like and subscribe.  

Rocking Rust - Building a USB Vendor Device with embassy-rs and the Raspberry Pi Pico - Playing with the Pico ep2  

Video content copyright (c) 2025 piers.media Limited. All rights reserved.  