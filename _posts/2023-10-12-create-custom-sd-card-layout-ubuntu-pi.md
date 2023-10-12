---
layout: post
title:  "Creating a custom SD card layout for Ubuntu 22.04 on a Raspberry Pi"
date:   2023-10-12 7:01 +0000
tags:   raspberry pi ubuntu sd card fdisk tune2fs mkfs.ext mkfs.vfat
---

I run an LTS release of Ubuntu on my main linux router and firewall, a Raspberry Pi 3B+ (why bother with anything more powerful?).  I forget why I went with Ubuntu, rather than Raspberry Pi OS as I use on all my other machines, but there was a good reason at the time.

Aside - I recall 2 possible reasons for using Ubuntu:
* At least at one point I had problems with pppd on Raspberry Pi OS, but it works fine for me on Ubuntu.
* Historically my router has been an x86 machine, so I used to use Ubuntu, and I just roll my existing service configs (like dhcpd and bind) to the new machine when I upgrade - sticking with Ubuntu makes this easier.

However the default Ubuntu 22.04 install left me with a 256KB ```/boot/firmware``` partition, which sits at 90% full, as Ubuntu keeps a backup copy of all the firmware on this parititon.  That doesn't leave a lot of spare capacity for the firmware and kernel to grow, so I wanted to re-layout the SD card, and at the same time downsize from a profligate 128GB SD card that I initially used to a (marginally) cheaper 32GB one.

## Backup existing SD card

I first powered down the Pi router, removed the SD card and installed in another linux machine.  Assume here that this was detected as ```/dev/sdg```.

First I backed up the parition 1:

```
sudo mount /dev/sdg1 /mnt
mkdir ~/existing_partition_1
sudo cp -a /mnt/* ~/existing_partition_1/
sudo umount /mnt
```

Then the second partition, which is much larger (around 5GB in my case):
```
sudo mount /dev/sdg2 /mnt
mkdir ~/existing_partition_2
sudo cp -a /mnt/* ~/existing_partition_2/
sudo umount /mnt
```

I then removed this SD card and kept it safe, in case something went wrong (which it did, read on).

## Create partition table on the new SD card

I used a pre-used/pre-0loved 32GB SD card from my loose micro-SD card drawer.  I inserted this in my other linux machine and it was detected as ```/dev/sdh```.

First I erased the first 8M on the card to ensure no partition table or existing filesystems were hanging around to confuse matters:

```
sudo dd if=/dev/zero of=/dev/sdh bs=512 count=16384 status=progress oflag=sync
```

The I ran fdisk as follows.

Launch fdisk:

```
sudo fdisk /dev/sdh
```

Create a new DOS partiton table:

```
o
```

Create a new DOS partition for /boot/firmware, making it 512MiB ((1050624-2048)*512 bytes) long:

```
n
p
1
2048
1050623
```

Mark this partition as bootable (probably not required for the Pi firmware to boot from it, but my existing Ubuntu SD card had the bootable flag set on partition 1, so I did this for consistency):

```
a
```

Change the partition type to FAT:

```
t
c
```

Now I created paritition 2, immediately following partition 1, and fill the rest of the SD card:

```
n
p
2
1050624
62333951
```

Print out the partition table (which at this stage hasn't yet been written to the SD card):

```
p
```

The output should be:

```
Disk /dev/sdh: 29.72 GiB, 31914983424 bytes, 62333952 sectors
Disk model: Storage Device
Geometry: 64 heads, 32 sectors/track, 30436 cylinders
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x0d9b3a83

Device     Boot   Start      End  Sectors  Size Id Type
/dev/sdh1  *       2048  1050623  1048576  512M  c W95 FAT32 (LBA)
/dev/sdh2       1050624 62333951 61283328 29.2G 83 Linux
```

Now write the parition table:

```
w
```

## Create filesystems for partitions 1 and 2:

First, create a FAT filesystem for 1st, boot, partition.  Here I label the volume ```system-boot``` as my existing Ubuntu SD card.  This may be necessary - not to boot the kernel - but for the OS to full boot, as ```/etc/fstab``` (which lives on partition 2) refers to it.

```
sudo mkfs.vfat -n system-boot /dev/sdh1
```

Now, create an ext4 filesystem for 2nd parition.  It is crucual this is given a volume name (label) of ```writable``` (note spelling!) as the kernel will look for a filesystem with this label to mount as the root filesystem.

```
sudo mkfs.ext -L writable /dev/sdh2
```

Check the volume name:

```
sudo tune2fs -l /dev/sdh2 | grep volume
```

Expected output:

```
Filesystem volume name:   writable
```

## Copy files from original SD card to new one

Now copy the files over from the original SD card, first parition one, which will mount to /boot/firmware:

```
sudo mount /dev/sdh1 /mnt
sudo cp -a ~/existing_partition_1/* /mnt/
sudo umount /mnt
```

Then the second partition:

```
sudo mount /dev/sdh2 /mnt
sudo cp -a ~/existing_partition_2/* /mnt/
sudo umount /mnt
```

Unmounting will likely take some time, as the OS will have cached the data to be written to the SD card in memory, in order to return to the shell sooner.  

## Enabke boot logging

As an optional extra I like to enable verbose boot logging from the kernel, like so.

First, mount the /boot/firmware partition:

```
sudo mount /dev/sdh1 /mnt
```

Now modify cmdline.txt:

```
sudo vi /mnt/cmdline.txt
```

Change ```quiet``` to ```verbose``` and remove ```splash``` so you end up with:

```
console=serial0,115200 dwc_otg.lpm_enable=0 console=tty1 root=LABEL=writable rootfstype=ext4 rootwait fixrtc quiet splash
```

Note the ```root=LABEL=writable```.  I mis-spelled the volume name as ```writeable``` when first creating the second partition, and it look me hours to track this down!

Unmount the parition again:

```
umount /mnt
```

## Ready to boot

A final ```sync``` command to be on the safe side (to ensure all data has been written to the SD card), and then  remove it and boot it up the Pi.

```
sync
```

## Results

Once booted, I logged in to check the /boot/firmware parition was the expected size, running:

```
df -k /dev/mmcblk0p1
```

This gave the expected result:

```
Filesystem     1K-blocks   Used Available Use% Mounted on
/dev/mmcblk0p1    523248 233316    289932  45% /boot/firmware
```

Hurrah.