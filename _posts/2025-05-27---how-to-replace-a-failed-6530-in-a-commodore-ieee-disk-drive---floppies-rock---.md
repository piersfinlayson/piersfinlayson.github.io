---
layout: post
title: "💾 How to Replace a Failed 6530 in a Commodore IEEE Disk Drive - Floppies Rock! 🔧"
date: 2025-05-27
categories: youtube
youtube_id: Yn1J9krukiE
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/Yn1J9krukiE" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

This week I test out my solution for a failed 6530 in a Commodore IEEE-488 disk drive - and it works!  

The 6530 is a factory mask programmed chip that provides RAM, ROM, IO and Timer (RRIOT) functionality. Unlike its sibling the 6532, it's a custom part specifically for these disk drives due to the ROM image and behaviour of the chip select pins. Finding an original replacement (part #901466) is nearly impossible.  

My solution repurposes a 6532 (still available), 74LS02 (quad NOR gate) and 27 series EPROM to replicate the original 6530 functionality.  

Need one of these boards? Available at: <https://piers.rocks/u/dd6530>  

A shout out to Ruud Baltissen, who's efforts here inspired my own: <http://baltissen.org/newhtm/6530repl.htm>  

⏱️ Timestamps  
00:00 🚀 Introduction  
00:19 📟 RIOT/RRIOT IC overview  
01:09 📋 6532/6530 pinout comparison  
04:13 📝 6530 replacement schematic  
05:40 🔄 6530 replacement PCB layout  
06:23 💡 6530 replacement in the flesh  
07:09 🧪 First test  
09:16 🎉 It verks!  
10:46 💭 Final thoughts  

Video content copyright (c) 2025 piers.media Limited. All rights reserved.  