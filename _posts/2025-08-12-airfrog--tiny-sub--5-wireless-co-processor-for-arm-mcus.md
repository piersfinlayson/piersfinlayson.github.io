---
layout: post
title: "Airfrog: Tiny sub-$5 wireless co-processor for ARM MCUs"
date: 2025-08-12
categories: youtube
youtube_id: XY2RdaR9DeU
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/XY2RdaR9DeU" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

Airfrog is a coin-sized wireless co-processor that gives you god-mode access to ARM MCUs over WiFi. Built around a $3 ESP32-C3 module, it adds processing power to the MCU, reprograms flash memory while the target continues running, extracts telemetry from systems with no spare processing cycles, and provides remote debugging capabilities without physical access to the target device.  

The project demonstrates live firmware updates on running systems, wireless data extraction from embedded devices, and integration with existing toolchains like probe-rs.  

Airfrog is written in Rust with libraries for writing custom firmware. REST and binary APIs enable network programming and control.  

Firmware, hardware designs, manufacturing files, and documentation are fully open source (MIT/CC-BY-SA-4.0).  

🔗 **Links**  

Airfrog: <https://piers.rocks/u/airfrog>  
Software Defined Retro ROM: <https://piers.rocks/u/sdrr>  

⏰ **Timestamps**  
00:00 🎬 Introduction  
00:28 🔧 Demo Setup  
00:50 🚀 Booting Airfrog  
01:19 💾 Updating RAM on running MCU  
02:22 ⚡ Updating flash on running MCU  
06:24 📡 Wireless co-processing  
08:31 ⭐ Other Airfrog features  
10:11 🎯 Accessing Pico/RP2040  
11:18 🛠️ Airfrog with probe-rs  
12:43 🎬 Wrap-up  

Video content copyright (c) 2025 piers.media Limited. All rights reserved.  