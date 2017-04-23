---
layout: post
title:  "Using Seeed Studio PCB Fab"
date:   2017-04-23 18:30:00 +0000
categories: esp8266 pcb seeedstudio
---

I've blogged a couple of times about getting PCBs fabbed - using both [OSH Park](https://oshpark.com/) and [Dirty PCBs](http://dirtypcbs.com).  A little while ago I got an out of the blue email from [Seeed Studio](https://www.seeedstudio.com/) asking me to try out their service.  I eventually got around to it, and I've just received my first boards back, so this post reviews the service.

To be clear - I received no discount or other compensation from Seeed Studio for this post (just as I've received nothing from OSH Park or Dirty PCBs for writing about their services).

# Ordering

Seeed Studio offer a big long list of options when ordering your PCBs:

* Material (FR-4, aluminium or flexible) - I chose standard FR-4

* Layers (1, 2, 4, 6, 8, 10, 12, 14 or 16) - I used 2

* Dimensions in mm - I was ordering around 60x75 which put me in the 100x100mm price bracket)

* Quantity (5-8,000) - I went for 10

* Panelized PCBs - A fairly complex option, which I didn't use (I was just having a single board fabbed)

* Thickness (0.6-3mm) - I went for the regular 1.6mm

* Soldermask colour (green, red, yellow, blue, white, black) - this time it was black's turn!

* Surface finish (HASL, HASL Pb free, ENIG, OSP, Hard Gold, Immersion Tin/Silver) - I went with the default/cheapest (HASL)

* Copper weight (1/2/3 oz) - 1oz

* Min Hole size (0.2mm, 0.25mm, 0.3mm) - I went with the largest/cheapest

* Min Tracking/Spacing (4/4mil, 5/5mil, 6/6mil) - again I went with the largest/cheapest

* Blind vias? - no for me

* Castellations - no

* Impedance control - actually I think they may have added this since I ordered!

All for a total cost of $9.90 plus $6.85 for the cheapest shipping option - $16.75 total.  This includes a $5 "Fusion shipping" discount - have no idea what this is for!

So how does the ordering process compare with OSH Park and Dirty PCBs?

Pros 

* Seeed Studio has far more options that the others.  OSH Park just offers a minimal set of options (ENIG mandated, 1oz 1.6mm or 2oz 0.8mm, medium run and super swift service).  Dirty PCBs has more options - but is lacking stuff like min hole size, sub 6mil traces, blind vias, castellations.

* Seeed can offer me other services - such as PCB assembly should I ever want to go down that route.

* I prefer Seeed's UI over Dirty PCBs new one (and old one!), but that may be a personal thing.

* Way cheapest!  Dirty PCBs wanted $25.95 inc shipping.  OSH Park would charge me $35.40 for 3 (instead of 10).

Cons

* Not really a con compared with the others, but I originally wanted to pay to get expedited (DHL) shipping.  The web UI wouldn't let me do this without an EORI/VAT number.  I don't have this and can't get one until I've actually submitted the first order and have an ETA for arrival into the UK - so reckon I would need to go through a manual process with Seeed the first time I want to do this.  I couldn't be bothered for these boards given the extra faff, so went with regular shipping.

* UI far more complicated than OSH Park.  But then it offers far more options.

* Neither Seeed nor Dirty PCBs accepted a kicad_pcb file - you have to convert your design into gerbers for both of these services.  Both do have a rendering facility so you can check what it will look like before submitting to fab though!

# The Wait

* I ordered from Seeed Studio on the evening of Thursday 6 April

* They went to fab early in the morning of Friday 7 April

* They shipped early morning Thursday 13 April (in line with promised 5 day fab)

* I received my boards (cheapest shipping option to the UK) Saturday 22 April.

That's just over 2 weeks.

The fastest I've received Dirty PCBs is just over 3 weeks - a week's fab and then 2 weeks shipping.  This _may_ just be variation in shipping times but read on...

OSH Park tend to come more quickly - I ordered some boards from OSH on 3 April, they went to fab same day, shipped 11 April and arrived 18 April.  That's the same elapsed time as Seeed - although there were a couple of public holidays in here as well.

There's no customs declaration on the Seeed package - I can't tell how it was shipped, nor what value was declared - it was relabelled in the UK (with a tracked, but not signed for option).  I don't think Dirty PCBs have ever come in this way, so Seeed may be using a better postal service.  Seeed calls their cheap option "US GB DE AU Post", whereas Dirty PCBs call theirs "Hong Kong Post Airmail".  Perhaps Seeed are bulk shipping boards to the UK where a partner is sending them on?

# The End Result

So how do the Seeed boards stack up?

They are very, very similar in quality to the Dirty PCB boards.  So similar it wouldn't surprise me if they were from the same fab house.

The picture below shows a Seeed board (left, in black) and a Dirty PCBs board (right, blue).  They are slightly different designs, but a good comparison.  Note also that the Seeed board is a KiCad design, the Dirty PCBs one from Eagle which explains the different fonts used in my silkscreens.

<img src="/static/img/seeed_vs_dirty_front.JPG" alt="Seeed Studio vs Dirty PCBS front"/>

<img src="/static/img/seeed_vs_dirty_rear.JPG" alt="Seeed Studio vs Dirty PCBS rear"/>

In fact, the boards are so similar I'm struggling to find any differences to pull out.  I've found two:

* Both producers put a code on the PCB, presumably so they can identify which is which after panelizing with others.  Dirty PCBs tend to put this on the front (which is annoying) - Seed have put it on the back which I prefer.  It's also in a different (and slighlty less obtrusive) font.

* I made a few mistakes with the Seeed silkscreen.  I left R44 and R45 silkscreens visible in KiCad, but actually overlapping the pads - the Seeed production process has moved these to the right of the resistors (and pushed the "1" next to R44 to the right).  There's a few other examples like this - I would much rather they just didn't print a silkscreen which overlaps the pad than change my design.  I don't know for sure Dirty PCBs wouldn't do this too though ...

Quality wise neither Dirty PCBs nor Seeed are a match for OSH Park.  The OSH Park boards a great quality - very few silkscreen defects, holes better centered, ENIG finish.  But you get what you pay for.

# Conclusion

Given the price different between Seeed and Dirty PCBs ($16.85 vs $25.95) and the practically indistinguishable quality I will be using Seeed again for any larger boards I produce where it isn't economic to use OSH Park.  My cut-off point for using OSH Park is between 1-2"x1-2", assuming I am OK with the 3 copies.

