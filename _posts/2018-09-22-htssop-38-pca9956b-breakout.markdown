---
layout: post
title:  "HTSSOP-38 PCA9956B Breakout Board"
date:   2018-09-22 15:30:00 +0000
categories: i2c pca9956 gpio
---

The [PCA9956B](https://www.nxp.com/docs/en/data-sheet/PCA9956B.pdf) is a 24-channel I2C driven constant current LED driver with PWM.  I'm going to be experimenting with this IC, but don't have any suitable breakout boards, so have knocked together a breakout board for this HTSSOP-38 package.

The breakout board is available to order on [OSH Park](https://oshpark.com/) below:
<p/>
<a href="https://www.oshpark.com/shared_projects/ODML4jKn"><img src="https://644db4de3505c40a0444-327723bce298e3ff5813fb42baeefbaa.ssl.cf1.rackcdn.com/a8dc502bb65e3d419e10a5c8bfc1b472.png" alt="PCB front" width="100"/></a>
<a href="https://www.oshpark.com/shared_projects/ODML4jKn"><img src="https://644db4de3505c40a0444-327723bce298e3ff5813fb42baeefbaa.ssl.cf1.rackcdn.com/0886aa1eaeaddd4c1be385a02bb4d238.png" alt="PCB read" width="100"/></a>

The datasheet recommends the corner pins (1, 19, 20, 38) have larger pads, presumably to help with wave soldering.  The IC also has a ground pad underneath which is included on the breakout board.
