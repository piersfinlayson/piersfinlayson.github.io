---
layout: post
title: "Accessing embedded ROM functions from Rust 🦀 with the Raspberry Pi Pico"
date: 2025-03-11
categories: youtube
youtube_id: vwEsO9Urdpo
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/vwEsO9Urdpo" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

Learn how to access microprocessor ROM functions directly from within your Rust code, and understand what approach Raspberry Pi took to make their ROM functions accessible from your applications.  

In this episode I demonstrate how ROM functions are locatable and callable on different micro-processors, including the ESP8266 and Raspberry Pi's RP2040, from within Rust.  While this topic is at a much lower level than most programmers get involved with, I've covered it in a simple, clear and approachable way so it should make sense to those with basic programming knowledge.  

This video covers:  
- Why you might want to access ROM functions directly - for performance, efficiency or to access low-level hardware capabilities  
- How ROM functions are stored and located on the ESP8266 - using a static linker map file  
- How ROM functions are stored and located on the RP2040 (the processor used in the Raspberry Pi Pico) - dynamically, using code and lookup tables located in the ROM  
- Accessing and calling RP2040 ROM functions within embedded Rust code  
- Why Raspberry Pi's solution is the most elegant I've seen, providing great usability and maintainability  

If you want to programmatically cause your RP2040/Pico to enter DFU mode from Rust, check out my rp2040-rom crate: <https://crates.io/crates/rp2040-rom>  


### Timestamps

00:00 Intro  
00:25 ESP8266 ROM functions  
02:56 RP2040 silicon  
03:55 RP2040 ROM functions  
11:30 Rust code to access ROM functions  
16:53 Summarising Rust access to ROM  
20:32 Conclusions and wrap-up  

Acknowledgements  

* I use a photo of a de-encapsulated RP2040 IC in this video, which is copyright @electronupdate. You can find his blog post about the Pico W silicon here <http://electronupdate.blogspot.com/2022/07/raspberry-pi-pico-w-silicon-level.html> and his youtube channel here <https://www.youtube.com/electronupdate.> I strongly recommend subscribing to his channel if you're interested in understanding more about how manufacturers implement their silicon.  

Links  

* rp2040-rom Rust crate: <https://crates.io/crates/rp2040-rom>  

* RP2040 bootrom source code: <https://github.com/raspberrypi/pico-bootrom-rp2040>  

* RP2040 datasheet: <https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf>  

If you found this video useful and interesting, please like and subscribe and comment down below!  

Rocking Rust - Accessing embedded ROM functions from Rust 🦀 with the Raspberry Pi Pico - Playing with the Pico ep3  

Video content copyright (c) 2025 piers.media Limited. All rights reserved.  