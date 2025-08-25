---
layout: post
title: "Building a USB Vendor Device with the Raspberry Pi Pico - Playing with the Pico ep1"
date: 2025-02-25
categories: youtube
youtube_id: f_c9s5aC1No
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/f_c9s5aC1No" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

In this episode, I demonstrate how to create a custom USB vendor device using the Raspberry Pi Pico and the TinyUSB stack. We'll look at a simple but complete example that implements both control and bulk transfers, following a subset of the protocol used by the xum1541 project (part of OpenCBM).  

Building a USB Vendor Device with the Raspberry Pi Pico - Playing with the Pico ep1  

This tutorial covers:  
- Setting up a basic USB vendor device  
- Implementing USB descriptors  
- Handling control and bulk transfers  
- Working with multiple cores on the Pico  
- Using the watchdog timer  


### Timestamps

00:00 Intro  
01:19 What is a custom/vendor device?  
02:27 Building & running the example  
07:59 TinyUSB stack configuration  
09:36 USB Descriptor code  
15:46 Example header file  
18:18 main.c  
24:20 Control transfer callback  
28:54 Bulk transfer callback  
33:39 Wrap-up  

The complete source code and documentation is available at:  
<https://github.com/piersfinlayson/tinyusb-vendor-example>  

This example is perfect for anyone wanting to:  
- Learn USB device development  
- Create custom USB peripherals  
- Understand low-level USB communication  
- Get started with the Raspberry Pi Pico  

Prerequisites:  
- Basic familiarity with C programming  
- Raspberry Pi Pico  
- Development environment set up for Pico  

Errata:  
- I implied that, if you run a watchdog on your Pico, you must start core 1, and feed the watchdog from that core as well as core 0.  That's not true - you only need to feed the watchdog from core 1 _if you have started core 1_ (which I am in this example for demonstration purposes).  
- The example may be incorrectly returning false from tud_vendor_control_xfer_cb() for transfers it doesn't want to handle.  It may be safest to return true for all unexpected/unhandled transfers.  

Video content copyright (c) 2025 piers.media Limited. All rights reserved.  