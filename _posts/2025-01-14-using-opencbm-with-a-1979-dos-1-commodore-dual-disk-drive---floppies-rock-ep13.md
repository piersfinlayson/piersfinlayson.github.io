---
layout: post
title: "Using OpenCBM with a 1979 DOS 1 Commodore dual disk drive - floppies rock ep13"
date: 2025-01-14
categories: youtube
youtube_id: sTCOTXtfprY
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/sTCOTXtfprY" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

In this episode, my goal is to remaster a Commodore DOS 1 demo disk.  This isn't easy because:  
* the DOS 1 disk format has a different layout (tracks/sectors) than a DOS 2 disk  
* OpenCBM doesn't work very well with DOS 1 units, or those with 2 disk drives  
* there doesn't seem to be an original image available.  

I spend much of my time digging through the OpenCBM source code and enhancing it to support my DOS 1 2040, and do eventually get a DOS 1 demo disk written and succeed in running a (passing) performance test on my 2040 with my PET.  However  I fell back to using the 4040 demo disk contents, written to a DOS 1 format disk formatted by my 2040.  

The playlist with other videos of me working on this 2040 is here: <https://www.youtube.com/playlist?list=PLXs34HaWLi10C6ZdFEMkyiR1x8duq9cft>  


### Timestamps

00:00 Intro  
01:53 OpenCBM 2040 identification  
24:15 DOS 1 OpenCBM status handling  
34:35 OpenCBM dual drive directory listing  
37:52 2040 demo disk images  
58:46 Testing with my PET  
63:58 Wrap-up  

Problems hit:  
* OpenCBM didn't correctly identify a DOS 1 2040 disk drive - I enhanced the source code to use a Memory Read (M-R) command that is compatible with both DOS 1 and DOS 2 drives.  
* OpenCBM didn't properly report the status of a DOS 1 2040 disk drive - I enhanced the source code to handle both DOS 1 and DOS 2 status reporting.  
* OpenCBM cbmcopy/cbmwrite doesn't properly write files to a DOS 1 2040 drive.  I have not diagnosed this problem - instead I worked around this as below.  
* The "2040 demo disk" d64 on zimmers.net is actually a DOS 2 4040 demo disk, not a 2040 disk.  I wrote this image to my DOS 2 2031 drive and copied the files over to a DOS 1 formatted disk, using my PET with both the 2040 and 2031 connected.  
* The 2040 demo disk in lynx (LNX) format, is not a list of original files - it also contains some games, and what look like some personal files.  I unlynxed this using cbmconvert 2.1, but didn't end up using the image.  

You can find my fork of OpenCBM, with the fixes I made, here: <https://github.com/piersfinlayson/OpenCBM>  
The 4040 demo disk labelled as 2040 demo disk is here: <http://www.zimmers.net/anonftp/pub/cbm/demodisks/drives/2040-demo.d64.gz>  
The lynxed 2040 demo disk files are here: <http://www.zimmers.net/anonftp/pub/cbm/demodisks/drives/2040DEMO.LNX.ZIP>  
cbmconvert is here: <http://www.zimmers.net/anonftp/pub/cbm/crossplatform/converters/unix/cbmconvert-2.1.2.tar.gz>  

Video content copyright (c) 2025 piers.media Limited.  All rights reserved.  