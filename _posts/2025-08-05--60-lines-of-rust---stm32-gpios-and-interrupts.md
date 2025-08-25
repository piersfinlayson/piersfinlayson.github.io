---
layout: post
title: "🦀60 lines of Rust - STM32 GPIOs and Interrupts"
date: 2025-08-05
categories: youtube
youtube_id: F6tI-qjXv_s
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/F6tI-qjXv_s" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

In this video I build a manufacturing test application for my Software Defined Retro ROMs in just 60 lines of Rust using embassy-rs.  I cover:  

* All of the steps required to set up an embedded STM32 Rust project from scratch.  
* Developing with asynchronous embassy tasks.  
* Using the defmt and RTT logging frameworks.  
* Driving an LED with an output pin.  
* Detecting input pin state changes with interrupts.  
* Flashing and testing using probe-rs.  

🔗 **Links**  

Finished code: <https://github.com/piersfinlayson/rs-stm32-gpios>  
probe-rs: <https://probe.rs/>  
embassy-rs: <https://embassy.dev/>  
Software Defined Retro ROM: <https://piers.rocks/u/sdrr>  

⏰ **Timestamps**  
00:00 🎬 Introduction  
01:31 📋 Application Overview  
02:06 🆕 New Rust project  
02:32 📦 Cargo.toml  
06:09 ⚙️ Cargo config.toml  
08:18 🔧 VSCode settings.json  
09:03 🔲 Rust STM32 target  
09:27 📝 Cargo.toml STM32 config  
09:54 🔗 Linker settings build.rs  
12:15 🚀 main() function  
15:00 💡 Flash LED  
22:54 📡 Programming STM32  
23:41 ⚡ GPIO interrupts  
30:10 🔄 6x interrupt tasks  
32:15 ✅ Final testing  
32:48 📊 Recap  
34:54 💭 Wrap-up  

Video content copyright (c) 2025 piers.media Limited. All rights reserved.  