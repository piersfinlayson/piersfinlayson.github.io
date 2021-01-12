---
layout: post
title:  "Using Seeed Studio's PCB Assembly Service"
date:   2021-01-12 7:00 +0000
tags:   seeed seeedstudio pcb pcba
---

Full Disclosure: I have not compensated in any way for this post by Seeed Studio (or anyone else).

# Introduction

I've been using [Seeed](https://www.seeedstudio.com/)'s [Fusion PCB](https://www.seeedstudio.com/fusion.html) fab service for some time now, but had shied away from using their [PCB Assembly](https://www.seeedstudio.com/prototype-pcb-assembly.html) (PCBA) service through fear of the unknown:
* It's relatively expensive - 10 of my main product design cost $300 to take all the way through PCBA, compared to $5 (more like $20 with shipping) for just the PCBs.
* I wasn't convinced of the quality of either parts or production I'd get.
* There were a few components on my design which aren't in their [Open Parts List](https://www.seeedstudio.com/opl.html) (OPL) which they recommend selecting from to shorten production time.
* I have a few non SMD parts in my design, and wasn't sure if these would be supported, or what the quality of soldering would be (in particular whether they'd be flush with and square to the board as they need to be for my design to work).

So, instead I've been hand soldering 100s of boards in my weekends [to sell](https://www.packom.net/).

I took the plunge late 2020 testing the PCBA service for 10 of my boards, and more recently ordered a batch of 100.  I've been very happy with the PCBA service I've received from Seeed, and the quality of the boards - and am now able to save myself considerable time in producing products for sale.

As I struggled to find any reviews of Seeed's PCBA service before using it, I'm writing up my findings in this post.

# Design

My design is a [Hat](https://www.raspberrypi.org/blog/introducing-raspberry-pi-hats/) for Raspberry Pis, and I've ben [selling](https://www.packom.net/) it in modest quantities for a few years now.  It's a fairly straighforward design, with 30-40 almost entirely SMD parts - 0603 resistors, SOT-23s, etc.  It's perfectly within my capabilities to hand solder, but takes me 3-4 hours to complete around 10 boards (to the point where they're completely cleaned all of residues and ready to test).  That's a lot of labour.

Before going ahead with PCBA, I read Seeed's [Design For Manufacturing](https://www.seeedstudio.com/pcb-design-for-manufacture.html) (DFM) guide.

This goes through lots of details of considerations for the process including:
* What format design files need to be submitted in.
* Minimum and maximum board dimensions.
* Minimum trace width and spacing.
* Minimum distance between components and the edge of the board.
* Minimum distance between components.
* Recommended pad sizes/dimensions for reflow soldering.

A lot of this stuff is required for standard PCB fab, but component distances, pad sizes, etc, are different - and due to a combination of:
* Needing space for the pick and place and other machines to work.
* Reflow soldering with large pad sizes (that you might want for hand soldering) being less reliable, and more likely to lead to [component tombstoning](https://www.eurocircuits.com/blog/tips-tricks-why-do-components-tombstone/).

The main changes I made to my design for PCBA were:
* Slightly large gaps between components (I now typically aim for >1 mm between the same sizes of components, and a bit more for different types of components - the DFM guide gives precise limits).  Previously for hand-soldering boards I was happy to squish the components really close together.
* Moved to a single sided design - although Seeed does support SMD components on both sides (I think they glue components onto one side so they don't fall off when the board is heated the other way up).
* Removing a third party boost converter mezzanine board I had been using (and customizing) and integrating my own boost converter design onto the main PCB.
* Using reflow component footprints rather than hand-soldering sized ones.  (Typically using the built-in KiCad footprints.)

The last change turned out to be a bit annoying due to wanting to be able to hand-solder the same design in emergencies.  I can hand solder 0603 components on reflow pads no problem, but I sometimes struggle with other components like SOT-23-6s.  I tend to get bridges which I can clear with a milli-Paul of flux, but would rather not get them in the first place! 

# Assembly Files

Like PCB production you obviously need to provide board gerbers, but you also need to provide a bunch of other information to Seeed for PCBA:
* [Component position](http://support.seeedstudio.com/knowledgebase/articles/1911202-how-do-i-export-pcb-pick-and-place-xy-files-for) (XY) files for their pick and place machine to use.  In KiCad you produce a .pos file.
* A [BOM file](https://statics3.seeedstudio.com/files/20194/BOM%20Template.xlsx) listing all of your components and the reference designators of them.  I've generated this by hand, but there are KiCad plugins to produce automatically.
* [Assembly gerbers](http://support.seeedstudio.com/knowledgebase/articles/1911127-how-do-i-export-pcb-assembly-drawings-fabrication), showing all of the components and their reference designators.  In KiCad these are the F.CrtYrd anf F.Fab (and B. if necessary) layers.
* A photo of an assembled board.  I don't think this is mandatory, but I've included to make sure that the connectors get soldered to the correct side of the board.  Technically this shouldn't be necessary as the assembly gerbers should show this, but I wanted to be safe - the idea of desoldering 100 x 40-pin headers and resoldering them myself doesn't appeal.

# Component Selection and BOM file

I found this the most time consuming part of the process - going through Seeed's [Open Parts List](https://www.seeedstudio.com/opl.html) and choosing the components I wanted.

It's mostly tedious because you need to do it for every single passive (resistor, capacitor, etc) value that you have.  I have also tweaked my design to use a component on the OPL rather than my own choice of part - for example changing to a slightly different I2C EEPROM.

I would probably find this easier in future as I now have a base from which to start, but even a new resistor value would require going in and checking the OPL for the appropriate part.

Where I haven't been able to find a part on the OPL I've chosen a part from Chinese component supplier [LCSC](https://lcsc.com/) who Seeed seem to be able to source from no problem.  If you're using a custom part you give a link to the part on the supplier's website within the BOM (there's a column to do this) and they then come back to you telling whether they can source it or not and the price.

# Ordering and Pricing

Ordering is very similar to the PCB ordering process.  From the [Fusion PCB page](https://www.seeedstudio.com/fusion_pcb.html):
* Select your PCBs.  Upload your gerbers and choose your colour, size, quantity, etc.  Note that for reflowed boards you'll need an ENIG (gold-plated) finish to the boards.  If you don't select this the tool will once you select PCB Assembly.
* Select PCB Assembly.  Upload your assembly instructions (component position files, assembly gerbers and any other instructions/photos as a zip file).
* Select how many PCBA boards you want - obviously this needs to be the same as or less than the number of PCBs you selected.
* Add your BOM file.  The tool will parse this in real-time and tell you if it can't find the component on the OPL.  You can still submit the order in this case, but the price quoted will only be indicative, and Seeed will come back to (within 24 hours in my experience) with an updated quote you can pay to move ahead with the order.
* Decide whether you want your own stencil - you don't need to order one for Seeed to build your boards, only if you want one yourself.

Check out the price and then order.  You can obviously fiddle around with your BOM, design, quantities of boards, etc, to see if you can get a better price.

I found that my 10 assembled boards cost around $300 shipping included, but 100 boards only cost about $1200.  The main reasons for the much reduced 100 board price were:
* Reduced PCB fab cost (for 100 vs 10 ENIG boards).
* Fixed setup cost.
* Fixed component wastage cost (the number of components that get lost loading and unloading the pick and place machine).

As Seeed provide free shipping, the best option is via DHL - this typically takes 4 working days for me based in the UK.  However, to use this option you need to provide a VAT or EORI number (I already had an EORI number as once now needed to do business with the EU post-Brexit) and DHL will collect any import duty from you online before delivery.  I got charged about £70 for the 10 boards and £200 for the 100 boards.  This includes DHL's admin fee.

I would advise avoiding Fedex - I've not used Fedex with Seeed, but LCSC sometimes use them and they are super slow from China.

For UK folks post 1 January 2021 it may be that Seeed now charge VAT on all orders on their website.  I haven't ordered yet this year, but [aliexpress](https://aliexpress.com/) are nowing doing so.

# DFM Review

All Seeed PCBA orders currently including a DFM review by them for free - although previously this has only been for orders above a certain value.  I would expect the DFM to remain free to all in future because I think the exercise is almost entirely automated.

My first PCBA order failed this review due to one issue.  I had included a SOT-23-6 (6-pin) pad but told them to install at SOT-23-5 (5-pin) component.  This was actually deliberate - my design uses a generic boost converter chip which comes in both 5 and 6 pin SOT-23 variants, and which are pin compatible if you don't use the 5th pin (I don't), and I wanted to keep the ability to swap out the chip for an alternative if necessary.  But rather than argue the toss I sent back a design with a SOT-23-5 pad and the design was accepted.

My second order (a larger quantity of the same board) got through DFM unscathed - as you'd expect as it was the same design as the first.

I strongly suspect the only reason for getting through DFM so smoothly was lots of reading of the DFM and then sticking to those guidelines pretty rigidly, and in fact I generally have them loaded in as design rules to KiCad for all of my future designs, including ones I intend to hand-solder.

# Testing and Commissioning

The ordering page indicates that you can get Seeed to perform custom test and commissioning processes on your boards - you need to give them instructions and presumably any necessary equipment - and they will quote for this separately.  I haven't done this.

# Production Process and Timeframe

Seeed provide a decent view of where the process is at via the Orders page within your account - it shows PCB production, component sourcing and assembly progress.

My first order of 10 boards took 2 weeks between ordering and shipping, including the DFM query I mentioned above and also resolving an issue with them being unable to supply a component that was on the OPL (I intended pointed them at an LCSC part which they were happy to use for the same price as the OPL part).

My second order of 100 boards took 3 weeks between ordering and shipping.  There were no queries that needed turning around this time, but it was over Christmas which may have slowed this process down.

# Quality

The boards arrive well packaged in a sturdy cardboard box with plenty of bubble wrap.  Each board is that individually wrapped in what I assume is anti-static (pink) bubble wrap, and well secured within the box.

Each board I've received has been in good condition:
* The quality of the PCB is exactly as I've come to expect from Seeed (which is good).
* The component placement is accurate.
* The soldering is extremely neat (much better than I could achieve by hand!).
* Even the through-hole headers have been fine - I'm not 100% how these have been attached, but it looks like the headers have been glued on (perhaps by machine) and then hand-soldered, although there is no flux residue anywhere on the boards so they were subsequently cleaned.
* There have been no solder bridges.
* Every board has worked fine without needing any hand touch-up.

So, all in all I've been very happy with the process and finished product.

# Conclusion

It's a bit of a pain going through the process for the first time - taking an existing design which wasn't designed for PCB Assembly and putting it through that process.

However, it's definitely worthwhile - for boards I ever expect to produce in quantities of over ~25 boards I will likely plan on having them assembled.  Therefore I will be using Seeed's DFM guidelines and choosing OPL parts wherever possible from day one.

A further step is to explore the testing and commissioning services Seeed can offer - again I would expect going through this process the first time to be painful as I might been to develop new equipment and iterate through the processes for a while.  As this would save me much less time than the PCBA process I'm not expecting to do it for now.



