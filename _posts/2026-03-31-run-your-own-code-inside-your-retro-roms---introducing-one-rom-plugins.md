---
layout: post
title: "Run your own code INSIDE your retro ROMs - introducing One ROM plugins"
date: 2026-03-31
categories: youtube
youtube_id: cpK3RSMJc8c
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/cpK3RSMJc8c" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

In this video I explain how you can run your own code within the most flexible replacement ROM for your retro systems, One ROM.  Plugins run on One ROM's two spare ARM Cortex-M33 150MHz cores, in parallel with One ROM serving a ROM to the retro system.  

I demonstrate the blinky and live USB stack plugins, including what they do and how they were written, and show you how to get started with writing your own plugins.  

I also cover:  
* How to monitor and modify One ROM live, while it's running, using the USB plugin and One ROM's new CLI.  
* picobootx - an open source PICOBOOT implementation you can include in your own firmware, allowing it to be managed by tools like picotool and picoflash directly, without being in BOOTSEL mode.  
* pico-sdkless - build projects like tinyusb for the RP2350 without needing the full Pico SDK.  

🔗 **Links**  

Discord: <https://discord.gg/tq22nJefXr>  
Buy: <https://onerom.org/buy>  

One ROM Plugin API: <https://github.com/piersfinlayson/one-rom/blob/main/sdrr/ora/api.h>  
Picobootx: <https://github.com/piersfinlayson/picobootx>  
Pico-sdkless: <https://github.com/piersfinlayson/pico-sdkless>  
picoflash: <https://picoflash.org/>  

⏰ **Timestamps**  

00:00 Introduction  
01:37 USB Plugin  


Video content copyright (c) 2026 piers.rocks Limited. All rights reserved.  