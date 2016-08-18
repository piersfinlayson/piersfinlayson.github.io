---
layout:  post
title:   "A rant about hobbyist software libraries"
date:    2016-08-18 19:00:00 +0000
categories: rant hobbyists libraries
---
# Hobbyist Software

Have spent this evening playing with a [PCA9685](http://www.nxp.com/products/power-management/lighting-driver-and-controller-ics/i2c-led-display-control/16-channel-12-bit-pwm-fm-plus-ic-bus-led-controller:PCA9685) 16 channel 12-bit PWM I2C GPIO controller.  I'm looking to use it to control a generic module which can itself drive lots of other stuff - like relays, LEDs, motors, etc.

This is the first time I've used this chip, so after soldering the TSSOP-28 to a prototype board and wiring the whole thing together I went looking for a library to talk to the device - it should get me running quickly, right?

I chose what looked to be a reputable one, compiled an example sketch and gave it a whirl.  Nothing.  After many hours and cursing I found a rectified a whole swathe of problems - from my poor TSSOP soldering, to a broken jumper wire (grrr!).  Once I solved all these issues the library just worked.  Great, huh?!

This is where the rant comes in.  While the software I found worked - once the hardware was all tip-top - it gave me no hints anything was awry, it just thought it was happily talking to the device over the I2C bus.  Well, it wasn't, and it _should_ have known this, as I2C includes a mechanism to ensure the slave has received instructions from the master - the ack.  Because the software I downloaded and used didn't check the ack, it couldn't and didn't provide any feedback to me that there was a problem.  I just had to guess the comms over I2C was broken.

This is all too common in the hobbyist electronics world - stuff that is designed to work only when everything is perfect, and to give no helpful clues if something isn't working.  It means everything is far too fragile, and is what lead me to develop otb-iot in the first place - and to use the ESP8266 SDK directly rather than use the (at the time) quite buggy and unstable Arduino port.

I realise the software I download is worth what I paid for it (nothing), but it sometimes feels like a false economy.  Could I have actually written a PCA9685 driver in less time than I spent trying to get this thing working today?  Perhaps not, but I want to write my own driver long-term anyway (as the whole point of otb-iot is to work, and be maintainable and supportable), so I probably should have bitten the bullet.  Especially given I've already written my own ADS1115 I2C driver so have a head start.  And it checks acks!

Lesson learned?  Probably not - I like free!
