---
layout: post
title: "🤖💪 Human vs Compiler - ARM cycle level ARM assembly optimization"
date: 2025-07-29
categories: youtube
youtube_id: GUVc9ohvqDI
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/GUVc9ohvqDI" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

This video is a (very) deep dive into the main ROM serving algorithm from the Software Defined Retro ROM, running on an STM32F4 (Cortex-M4) MCU, covering  

* the default hand-crafted assembly algorithm, in detail, explaining all of the key performance optimizations  
* the most highly optimized assembly the GCC compiler can achieve from two different C implementations  
* why I don't use interrupts (they just are not fast enough for this use case, on this processor)  

The results may surprise you.  

If you think you can do better - post your code in the comments below!  

🔗 **Links:**  
Software Defined Retro ROM (SDRR) github repo: <https://piers.rocks/u/sdrr>  
SDRR intro: <https://youtu.be/Jhe4LF5LrZ8>  
SDRR tech deep dive: <https://youtu.be/pOZ2-W3dpZ8>  

⏰ **Timestamps**  
00:00 🎬 Introduction  
00:10 🧪 Test Methodology  
01:50 📊 Results  
02:25 💪 Hand Rolled Assembly  
12:38 🔧 Naive C Implementation  
16:15 🚀 Better C Implementation  
26:35 ⚡ Interrupts - Why Not?  
27:53 💭 Final Thoughts  

Video content copyright (c) 2025 piers.media Limited. All rights reserved.  