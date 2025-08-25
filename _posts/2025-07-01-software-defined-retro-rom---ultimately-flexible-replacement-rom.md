---
layout: post
title: "Software Defined Retro ROM - ultimately flexible replacement ROM"
date: 2025-07-01
categories: youtube
youtube_id: Jhe4LF5LrZ8
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/Jhe4LF5LrZ8" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

A drop-in ROM replacement for vintage 8-bit computers that solves the fundamental limitations of existing solutions. Built around an STM32F4 microcontroller, SDRR delivers true flexibility, replacing 2364, 2332 and 2316 ROMS, through software configuration while fitting in the exact footprint of the ROM socket.  

This video introduces the project and demonstrates why existing ROM replacements fall short - from inflexible hardware configurations requiring physical modifications, to tedious programming workflows that interrupt development, to bulky adapters that may not fit properly in existing systems.  

SDRR addresses these problems with a software-defined approach: configure ROM types and chip select behavior through makefile configuration, reprogram in-system via 3-wire SWD without removing the chip, and achieve all this in a compact design that fits the original 2364/2332/2316 ROM footprint.  

Live demonstrations show SDRR working in C64 and VIC-20 systems, including real-time reprogramming and configuration changes. The complete solution costs under $5 per board in low volumes (much cheaper in high volumes) and is fully open source.  

Perfect for diagnostics, development, system restoration, and anyone working with PET, C64, VIC-20, IEC and IEE disk drives, and other 8-bit systems requiring 2364, 2332, or 2316 ROM replacements.  

Github Repo: <https://piers.rocks/u/sdrr>  

⏰ **Timestamps**  
00:00 🚀 Introduction  
00:12 📋 Background  
01:33 🔒 Today's ROMs - inflexible  
02:46 ⏳ Today's ROMs - tedious programming  
04:26 📦 Today's ROMs - bulky replacements  
05:15 🎯 Solution - flexibility  
05:47 ⚡ Solution - easy programming  
06:16 📏 Solution - compact  
06:26 💰 Solution - low cost  
06:48 🔓 Solution - fully open source  
07:00 🖥️ Demo - C64 kernal  
07:50 🔧 Demo - C64 dead test ROM  
08:26 🎨 Demo - C64 character ROM  
09:34 🔄 Demo - reprogramming in-situ  
12:09 ⚙️ Demo - ROM config  
13:46 🛠️ Demo - building and flashing  
14:55 🎮 Demo - Vic-20 dead test ROM  
15:34 📂 Open source  
15:47 💸 Build cost  
16:28 🎬 Wrap up  

Video content copyright (c) 2025 piers.media Limited. All rights reserved.  