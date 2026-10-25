---
layout: post
title: "Laying out a 40 pin 16-bit One ROM - Amiga Kickstart support coming soon?"
date: 2026-01-13
categories: youtube
youtube_id: nt8YBvBbD7E
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/nt8YBvBbD7E" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

In this video I show how I laid out a new 40 pin version of the One ROM, which is intended to support 16-bit systems like the Amiga, using the B variant of the Raspberry Pi RP2350/RP2354.  I cover:  
- the 27C400 ROM chip often used in these 16-bit systems  
- the constraints on the layout due to my firmware design  
- laying out the PCB in KiCad, starting from a copy of the 28 pin One ROM Fire layout  

🔗 **Links**  

One ROM website: <https://onerom.org/>  
16-bit firmware design: <https://github.com/piersfinlayson/one-rom/discussions/69#discussioncomment-15436012>  
An alternate design by a subscriber: <https://github.com/going-digital/A600ROM/tree/main/hardware>  

**Buy One ROMs**  

Keep an eye on my online store if you want to buy One ROMs when they are available:  

<https://www.packom.net/product/one-rom/>  

If you sell a version of One ROM, let me know so I can publicise it on youtube and at <https://onerom.org/>  

⏰ **Timestamps**  

00:00:00 Introduction  
00:03:20 16-bit ROM  
00:06:24 Schematic differences from 28 pin  
00:07:52 Layout constraints  
00:14:00 Starting PCB layout from 28 pin  
00:20:10 Ripping the 28 pin design apart  
00:22:20 Placing new components  
00:26:12 Starting to route traces  
00:28:48 Assembly constraints  
00:29:57 Routing 16-bit data bus  
00:42:06 Voltage rails  
00:45:11 Address lines routed  
00:46:22 Bypass capacitors  
00:49:27 Crystal oscillator  
00:50:19 More bypass capacitors  
00:53:42 VREF circuitry  
01:02:31 Flash chip laid out  
01:06:46 Adding more features  
01:17:53 Layout complete  
01:20:54 Final thoughts  

Video content copyright (c) 2026 piers.rocks Limited. All rights reserved.  