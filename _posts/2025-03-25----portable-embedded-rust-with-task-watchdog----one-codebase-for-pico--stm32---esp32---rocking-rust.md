---
layout: post
title: "🛡️ Portable Embedded Rust with task-watchdog 🐺: One Codebase for pico, stm32 & esp32 | rocking rust"
date: 2025-03-25
categories: youtube
youtube_id: v4u39KzBkBo
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/v4u39KzBkBo" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

Learn how to build robust embedded applications using Rust, Embassy, and my new task-watchdog crate - a flexible watchdog management library that multiplexes task watchdogs into a single hardware watchdog timer!  

In this two-for-one video, I demonstrate how to write truly portable embedded code that works across multiple microcontroller platforms (Raspberry Pi Pico/Pico 2, STM32, and ESP32) using the same codebase, while showcasing my new task-watchdog crate for managing system reliability.  

This video covers:  

- 🛡️ Understanding watchdogs and why they're critical for embedded system reliability  
- 🔀 How task-watchdog multiplexes multiple task watchdogs into a single hardware watchdog  
- 💻 Writing portable Rust code that works across Pico, Pico 2, STM32, and ESP32  
- ⚡ Using Embassy for async Rust on embedded systems  
- 🧠 Building a complete multi-task application with proper watchdog integration  
- 🔌 Dynamic task management with runtime registration/deregistration  
- 🚫 Demonstrating fault recovery with intentional task failures  

I start with a basic example showing the core API, then expand to a more comprehensive example that supports all target platforms in a single file, demonstrating the true portability of both task-watchdog and Embassy-based embedded Rust.  

Whether you're building mission-critical embedded systems or just want to make your projects more robust, this video will show you how to implement proper watchdog management across multiple platforms with a single, clean codebase.  


### Timestamps

00:00 Introduction  
00:20 Why watchdogs matter  
01:53 The task-watchdog approach  
03:50 Basic example walkthrough  
07:09 Multi-platform demonstration  
09:49 Portable code walkthrough  
14:43 Wrap-up and learnings  

I didn't cover the full task-watchdog API in the video, so check out the crate documentation below if you're interested.  In particular there's also a task_deregister() call, which allows tasks to block without the watchdog being triggered.  

Links:  

- task-watchdog crate: <https://crates.io/crates/task-watchdog>  
- GitHub repository: <https://github.com/piersfinlayson/task-watchdog>  
- Embassy-rs framework: <https://embassy.dev>  

If you found this video useful, please like and subscribe, and let me know in the comments what topics you'd like to see covered next!  

Video content copyright (c) 2025 piers.media Limited. All rights reserved.  

All Espressif's logos are trademarks of Espressif Systems (Shanghai) Co., Ltd.  