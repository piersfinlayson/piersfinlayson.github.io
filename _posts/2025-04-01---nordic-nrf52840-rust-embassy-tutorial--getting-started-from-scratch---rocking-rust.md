---
layout: post
title: "🔷 Nordic nRF52840 Rust Embassy Tutorial: Getting Started from Scratch | rocking rust"
date: 2025-04-01
categories: youtube
youtube_id: _GnU1bThTpc
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/_GnU1bThTpc" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

🎮 Ready to add Nordic nRF52840 to your multi-platform Rust arsenal? This tutorial walks you through setting up and running Embassy applications on the powerful Nordic nRF52840 Bluetooth-capable microcontroller!  

Following up on my task-watchdog video, I'm expanding our portable embedded Rust journey to include Nordic devices. This step-by-step guide shows you exactly how to configure, build, and run Rust Embassy applications on the nRF52840 from complete scratch.  

This video covers:  

* 🔷 Introduction to the Nordic nRF52840 capabilities and features  
* 🛠️ Setting up the complete development environment for nRF52840  
* 📄 Creating and understanding all required config files (main.rs, Cargo.toml, .cargo/config.toml, build.rs, memory.x)  
* 💡 Building a basic LED blink example with Embassy  
* 🐺 Extending the task-watchdog library to support nRF devices  
* 🧩 Adapting portable code patterns to work across all platforms (Pico, STM32, ESP32, and now nRF)  

I start with absolute basics so you can follow along even if you've never touched a Nordic device or Embassy before, and progress to integrating our task-watchdog examples from the previous video, demonstrating true cross-platform portability.  

Whether you're interested in Bluetooth applications, ultra-low power devices, or just expanding your embedded Rust skills to another platform, this tutorial start you on the journey of building robust applications on the nRF52840.  


### Timestamps

00:00 Introduction to nRF52840  
01:00 Pre-requisites  
01:43 main.rs  
06:04 Cargo.toml  
07:44 .cargo/config.toml  
09:16 Installing Rust target  
10:11 SWD support  
12:34 memory.x and build.rs  
14:07 It verks!  
14:54 Task-watchdog integration for nRF  
18:49 Wrap-up  

Links:  
* Embassy nRF support: <https://docs.embassy.dev/embassy-nrf/>  
* nRF52840 Product Page: <https://www.nordicsemi.com/Products/nRF52840>  
* task-watchdog crate: <https://crates.io/crates/task-watchdog>  
* GitHub repository: <https://github.com/piersfinlayson/task-watchdog>  

If you found this video useful, please like and subscribe, and let me know in the comments what other platforms or topics you'd like to see covered next! 💻🚀  

Video content copyright (c) 2025 piers.media Limited. All rights reserved.  