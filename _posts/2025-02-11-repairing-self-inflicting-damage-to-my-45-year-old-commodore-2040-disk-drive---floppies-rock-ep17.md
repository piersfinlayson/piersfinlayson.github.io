---
layout: post
title: "Repairing self-inflicting damage to my 45 year old Commodore 2040 disk drive - floppies rock ep17"
date: 2025-02-11
categories: youtube
youtube_id: uDdH7GuyNEc
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/uDdH7GuyNEc" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

In the world of vintage computing, sometimes we're our own worst enemy. After accidentally damaging my DOS 1 Commodore 2040 disk drive, I take you through the diagnosis and repair of its IEEE-488 circuitry.  

Repairing self-inflicting damage to my 45 year old Commodore 2040 disk drive - floppies rock ep17  

In this episode, I track down why my DOS 1 Commodore 2040 disk drive has stopped talking to me.  The culprit?  A failed MC3446N bus transceiver that handles the vital IEEE-488 communication protocol.  

Follow along as I use an multimeter, oscilloscope, and service manual schematics to track down this communications fault.  You'll see practical debugging techniques for tracking down digital bus problems in vintage hardware.  


### Timestamps

00:00 Intro  
01:11 Symptoms  
03:16 Schematic  
05:35 Initial diagnosis  
10:25 Testing with oscilloscope  
18:40 Replaced bus transceiver  
23:40 It verks!  
25:25 Wrap-up  

Problems:  
* While the disk drive appeared to boot OK, the device I used to connect to the disk drive was hanging when I attempted to talk to it.  
* I tracked down the problem to a failed MC3446N bus transceiver, UB2.  
* I replaced the MC3446N with one pillaged from another of my IEEE-488 drives.  This resolved the problem.  
* I suspect I either shorted out some IEEE-488 pins or introduced some static to the bus to cause the bus transceiver to fail.  

You can find the other videos about my 2040 here: <https://www.youtube.com/playlist?list=PLXs34HaWLi10C6ZdFEMkyiR1x8duq9cft>  

Video content copyright (c) 2025 piers.media Limited.  All rights reserved.  