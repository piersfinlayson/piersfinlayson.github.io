---
layout: post
title: "How it's done - Software Defined ROMs"
date: 2025-07-08
categories: youtube
youtube_id: pOZ2-W3dpZ8
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/pOZ2-W3dpZ8" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

The engineering deep-dive behind Software Defined Retro ROM: real-world MCU selection criteria, schematic design failures, PCB layout decisions, and embedded implementation choices that made nanosecond ROM emulation possible.  

This video breaks down the technical decisions behind SDRR - from why I didn't choose the Pico, ATMEGA or STM32F103, to PCB layout and routing in a two layer compact form factor, finishing off with scoping the working solution.  

Previous video (introduction): <https://youtu.be/Jhe4LF5LrZ8>  
Github repo: <https://piers.rocks/u/sdrr>  

⏰ **Timstamps**  
00:00 🚀 Introduction  
00:44 📄 Original ROM datasheet  
05:13 📝 Requirements  
06:55 ⚠️ Constraints  
08:49 🎯 MCU Family Selection  
13:19 ❌ STM32F1 (Failed) Schematic  
17:40 ✅ STM32F4 Schematic  
22:16 🔌 PCB Layout  
25:00 💾 ROM Code  
29:33 🔬 Scoping the Software ROM  
31:15 🎬 Wrap up  

Video content copyright (c) 2025 piers.media Limited. All rights reserved.  