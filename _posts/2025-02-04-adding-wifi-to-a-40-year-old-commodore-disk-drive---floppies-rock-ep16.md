---
layout: post
title: "Adding WiFi to a 40 year old Commodore disk drive - floppies rock ep16"
date: 2025-02-04
categories: youtube
youtube_id: bLjhrWTavpM
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/bLjhrWTavpM" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

Transform your Commodore 1541 disk drive into a WiFi-enabled storage device!  Watch as I merge 1980s computing with modern networking, letting you access classic floppies from any Linux PC without wires.  

Adding WiFi to a 40 year old Commodore disk drive - floppies rock ep16  

In this episode, I went a bit mad, and installed an xum1541 and Raspberry Pi Zero W into one of my Commodore 1541 disk drives.  I then accessed it from my Linux PC using a few different Rust projects.  See below for links to the source code.  


### Timestamps

00:00 Intro  
00:36 1541 access via WiFi  
01:52 Mount as a linux filesystem  
03:08 Access 2 drives via WiFi  
04:17 Harware modifications  
05:18 Software overview  
06:47 Further thoughts  

xum1541 source code is here: <https://github.com/piersfinlayson/xum1541>  
* To build the software for your own WiFi 1541 follow intructions in docs/REMOTE.d  

rs1541 source code is here: <https://github.com/piersfinlayson/rs1541>  
* To run the CLI, use cargo run --examples cli -- --remote --remote-addr your-drive  

The rs1541fs source code is here: <https://github.com/piersfinlayson/rs1541fs>  
* This includes 1541fsd and 1541fs shown in the video  

Video content copyright (c) 2025 piers.media Limited.  All rights reserved.  