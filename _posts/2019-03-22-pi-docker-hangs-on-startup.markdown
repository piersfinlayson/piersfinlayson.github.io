---
layout: post
title:  "Docker on Raspberry Pi hangs on startup"
date:   2019-03-22 19:02:00 +0000
categories: rpi raspberry pi docker hangs startup
---

I recently discovered that on at least one of my Raspberry Pi's [docker](https://www.docker.com/) was hanging on boot - for the order of 10 minutes or so.  Manual attempts to start/restart docker hit the same issue.

I tracked down the apparent cause for the hang to this output from dmesg, which appeared immediately before docker (finally) started:

```
Mar 17 19:36:38 pi5 kernel: [  692.320127] random: crng init done
Mar 17 19:36:38 pi5 kernel: [  692.320140] random: 7 urandom warning(s) missed due to ratelimiting
```

Turns out that the random number generator /dev/random was taking substantial time to gather enough entropy to properly initialize, and docker was waiting for /dev/random.  The fix here was to install [haveged](https://issihosts.com/haveged/) which is a software random number generator, and which generates entropy for the system instead.

Haveged is installed by:

```
sudo apt install haveged
```

After installing haveged, on the next boot docker started in a much more timely fashion!