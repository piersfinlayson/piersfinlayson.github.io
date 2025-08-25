---
layout: post
title: "Precise Timing with Embassy & Rust on the Raspberry Pi Pico - Playing with the Pico ep4"
date: 2025-03-18
categories: youtube
youtube_id: GFFq-5S_QUY
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/GFFq-5S_QUY" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

Learn how to achieve precise timing in your embedded Rust applications using Embassy, from milliseconds down to nanoseconds.  

This video explores the various timing mechanisms available in the Embassy framework for the Raspberry Pi Pico and Pico 2, comparing their accuracy, multi-tasking capability, and resolution.  I'll cover both the theory and practical implementation with real oscilloscope measurements to demonstrate how each approach performs in the real world.  

This video covers:  
* An overview of different timing mechanisms in Embassy  
* Why timing precision matters in embedded applications  
* Comparing Timer::after(), Timer::at(), Delay methods, and assembly implementations  
* Performance differences between Raspberry Pi Pico and Pico 2  
* Achieving sub-microsecond timing precision  
* Real-world demonstrations with oscilloscope measurements  
* Practical recommendations for when to use each timing approach  

If you need precise control over GPIO timing in your Pico projects, this video will help you understand which mechanisms best suit your application needs.  

### Timestamps

00:00 Intro  
00:45 Embassy & async  
05:16 Using embassy-time  
10:30 Piers's Top Tips  
13:55 Timer::after_micros() demo  
17:57 Delay.delay_us() demo  
20:52 cortex_m::asm::delay() demo  
22:19 Inline assembly demo  
28:52 Wrap-up  

Links:  

Embassy-rs framework: <https://embassy.dev>  
Embassy timing documentation: <https://docs.embassy.dev/embassy-time/>  
Test code from this video: <https://github.com/piersfinlayson/embassy-pico-test>  
Raspberry Pi Pico documentation: <https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html>  

If you found this video useful and interesting, please like and subscribe, and comment down below.  

Precise Timing with Embassy & Rust on the Raspberry Pi Pico - Playing with the Pico ep4  

Video content copyright (c) 2025 piers.media Limited. All rights reserved.  