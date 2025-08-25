---
layout: post
title: "💾 Brand new Commodore IEEE Disk Drive Diagnostic ROM | floppies rock"
date: 2025-04-08
categories: youtube
youtube_id: ojbuZWuedMY
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/ojbuZWuedMY" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

🛠️ In this video, I demonstrate a diagnostic ROM I developed for Commodore 2040, 3040, and 4040 disk drives. I created this while trying to fix a problematic 3040 drive and thought it might help others working on these vintage machines.  

💡 The ROM performs zero page and static RAM memory tests and uses the drive's LEDs to indicate what's wrong - making it easier to identify which chip has failed without needing specialized equipment.  

What's in the video:  
* 🔧 Why I made this diagnostic tool for my drives  
* 📖 How to use it  
* ✅ Testing in a working drive to show normal operation  
* 🔍 Demonstrating what happens with a faulty 6532/RIOT chip (causing zero page RAM issues)  
* 💾 Showing how it identifies bad static RAM chips  
* 🔢 Reading the drive's device ID and reporting it via LED flashes  
* 🔌 Installing it both as the primary ROM ($F000) and alongside stock DOS 1 ROMs ($D000)  

The ROM has been useful for my own repairs, letting me quickly pinpoint which components needed replacing.  Is my 2040 now the World's largest1 2114 static RAM tester??? 😄  

Timestamps  
00:00 Intro  
00:11 Why?  
00:31 What's in this video  
00:49 2040 Architecture Overview  
02:08 Diag ROM in action  
02:54 Zero page failure  
03:42 Static RAM failure  
05:07 Running alongside stock ROMs  
06:37 Source assembly  
06:58 Wrap-up  

Links:  
* 📂 GitHub repo: <https://github.com/piersfinlayson/cbm-ieee-disk-diag-rom>  
* ⬇️ ROM downloads: <https://github.com/piersfinlayson/cbm-ieee-disk-diag-rom/releases/>  

If you're working on old Commodore drives, hopefully this helps save you some debugging time. 💾  

Video content copyright (c) 2025 piers.media Limited. All rights reserved.  