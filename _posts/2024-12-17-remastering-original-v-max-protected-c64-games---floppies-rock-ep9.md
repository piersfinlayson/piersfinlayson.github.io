---
layout: post
title: "Remastering original V-MAX protected C64 games - floppies rock ep9"
date: 2024-12-17
categories: youtube
youtube_id: rkTAvoLRE_8
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/rkTAvoLRE_8" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

In this episode I run through the equipment and steps required to successfully re-master original games with V-MAX copy protection.  


### Timestamps

00:00 Intro  
00:22 Requirements  
02:59 OpenCBM and nibtools  
03:31 Plug in XUM1541/ZoomFloppy  
05:52 Reformat destination disk  
09:15 Using nibwrite to write disk  
10:50 It fails - and why  
12:44 Rewriting disk at 297.5 RPM  
13:34 It succeeds  
14:30 Wrap-up  

Equipment and software required:  
* OpenCBM - <https://github.com/OpenCBM/OpenCBM>  
* nibtools - <https://github.com/markusC64/nibtools>  
* A 1541 disk drive with a parallel port mod, or a stock 1570 or 1571.  
* An XUM1541 USB-CBM disk drive adapter - a ZoomFloppy is one implementation of the XUM1541 which will work.  
* A blank floppy disk.  
* A .nib or .nbz file containing the original game disk image you want to write.  

Really importantly, for a V-MAX copy protected disk you must adjust the speed of the drive your're writing the disk with to 297.5 RPM.  The game won't write successfully at 300 RPM.  But it will only load at 300RPM - it won't load at 297.5 RPM!  

Video content copyright (c) 2024 piers.media Limited.  All rights reserved.  