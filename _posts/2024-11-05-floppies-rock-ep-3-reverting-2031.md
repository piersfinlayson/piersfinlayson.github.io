---
layout: post
title:  "Video: Reverting a Commodore 2031 back from a 1541 (floppies rock ep 3)"
date:   2024-11-05 15:45 +0000
tags:   commodore 64 c64 pet ieee 488 ieee-488 gpib hpib 1541 disk drive floppy 5.25 2031 2031lp
---

Episode 3 in my [piers rocks](https://youtube.com/@piers_rocks) floppies rock series:

[![floppies rock ep 2](https://img.youtube.com/vi/hD0U8kDFsvc/0.jpg)](https://www.youtube.com/watch?v=hD0U8kDFsvc)

(opens in a new window)

I look at another Commodore 2031LP disk drive in episode 3 of floppies rock.  However, this 2031LP isn't quite what it seems, containing 1541 internals.  First I have to get it working as a 1541, before I can then mod it back to a 2031.

Timestamps:
00:00 Intro
01:48 Initial inspection
05:25 1541 testing
07:06 Speed adjustment
08:43 Inspecting the drive mechanisms
11:22 Tachometer testing
13:44 Explaining the 2031 mod
15:24 2031LP testing
17:25 2031 mod details
17:37 Main mod board
20:24 IEEE-488 connector cable
21:49 Replacement ROMs
24:04 Device number change
26:03 Wrap-up

Problem with existing drive:

* The only problem I found with the existing drive was that the spindle motor tachometer had failed and so was driving the motor much too fast.  When tested it high resistance across the winding (which should be of the region of 170 ohms).  The tachometer was still generating an AC signal but at 280mV instead of the 2.8V of a working unit.

I intend to fix this in a future video - for this video I replaced the drive mechanism with a known good one from another 1541.

You can find the 2031 patched top (E000-FFFF) ROM for use with a 1541 bottom (C000-DFFF) ROM here: https://github.com/piersfinlayson/piers.rocks.video.support

You can find more information about the mod here: http://www.zimmers.net/anonftp/pub/cbm/documents/projects/ieee-488/vc1541-ieee.tar.gz

The service manual for the 2031 (both HP and LP) is here: http://www.zimmers.net/anonftp/pub/cbm/schematics/drives/old/2031/2031_Disk_Drive_Service_Manual.pdf