---
layout: post
title: "PIOs Rock! - Blazingly fast retro ROM serving with no CPU and just 18 bytes of PIO code"
date: 2025-11-25
categories: youtube
youtube_id: Y8RODQZM2HY
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/Y8RODQZM2HY" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

I've added PIO support to One ROM Fire - and not just any PIO support, but a completely autonomous PIO+DMA chain that is over twice as performant as the existing CPU-based algorithm.  

This is a deep dive into how I use the PIOs and DMA together on the RP2350 for maximum performance, beating any other algorithm I've seen for ROM serving on microcontrollers.  

I also show off an anomoly that I can't explain in one of my VIC-II video chips, exposed by this algorithm.  

🔗 **Links**  

One ROM website: <https://onerom.org/>  

🛒 **Buy One ROMs**  

Keep an eye on my online store if you want to buy One ROMs when they are available:  

<https://www.packom.net/product/one-rom-ice-usb/>  

If you sell a version of One ROM, let me know so I can publicise it on youtube and at <https://onerom.org/>  

⏰ **Timestamps**  

00:00 🎬 Introduction  
01:25 ⚡ PIO+DMA performance  
02:22 ⚙️ PIO introduction  
05:30 🔀 DMA introduction  
06:13 🔄 PIO+DMA algorithm  
15:58 💻 PIO code walkthrough  
26:57 🎛️ DMA configuration walkthrough  
34:48 ⚖️ PIO+CPU comparison  
38:53 ⚠️ Marginal video chip?  
41:12 💭 Final thoughts  

Video content copyright (c) 2025 piers.rocks Limited. All rights reserved.  