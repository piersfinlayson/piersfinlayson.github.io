---
layout: post
title: "📡Remotely controlling a PET, using Linux and GPIB/IEEE-488"
date: 2025-04-29
categories: youtube
youtube_id: TYoed0XvLCo
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/TYoed0XvLCo" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

📂 GitHub repo: <https://github.com/piersfinlayson/pet-ieee-loader>  

This week I got distracted an implemented a remote control for the Commodore PET, driving it via GPIB (IEEE-488) and a Linux PC.  

Using this you can upload BASIC programs and machine code to the PET 4x faster than using a disk drive, and launch them without touching the PET.  

This allows you to:  
- streamline development workflows with a real PET (you can modify your code on a PC, and then upload and execute it immediately when you're ready)  
- getting programs onto your PET quickly if you don't have a working disk drive (for example, to load a utility to help you diagnose problems with a drive)  
- control multiple PETs simultaneously, launching the same code within a few microseconds.  

You'll need an xum1541/ZoomFloppy/pico1541 with GPIB/IEEE-488 support to connect your PET to your PC.  

Timestamp:  
00:00 Introduction  
00:34 Machine code demo  
01:19 BASIC demo  
02:31 How it works  
10:49 Uses  
13:24 Final thoughts  

Video content copyright (c) 2025 piers.media Limited. All rights reserved.  