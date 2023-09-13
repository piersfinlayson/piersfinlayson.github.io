---
layout: post
title:  "Basic DMA test program for the Pico"
date:   2023-09-13 7:00 +0000
tags:   raspberry pi pico sdk picotool bare metal dma
---

I've never used DMA before so wrote [this simple program](https://github.com/piersfinlayson/pico-samples/tree/main/dma) for a Pico (based heavily on [pico-examples/dma/hello_dma.c](https://github.com/raspberrypi/pico-examples/blob/master/dma/hello_dma/hello_dma.c)) to test the speed of a DMA transfer, how much work can be done during that transfer, and compare that to a memcpy of the same data.
* First it does a DMA transfer of a chunk of memory, 4 bytes at a time.
  * As this is DMA, the CPU is free during the transfer, so the CPU does some work (counts up).
* Then it does the same size memcpy, but this time doesn't have time to do any counting.

## Build

From the root of [this repo](https://github.com/piersfinlayson/pico-samples):

```
cmake .
make -j 4 dma
```

## Install

With your pico attached in BOOTSEL mode (as device sdx):

```
./flash-pico.sh sdx dma/dma.uf2
```

## Test

Connect a serial terminal, for example:

```
minicom -o -D /dev/ttyACM0
```

You should see output like the following:

```
DMA: DMA transfer of 16384 32-bit values took 132us, CPU counted to: 2048
DMA: memcpy of 65536 bytes took 479us, CPU didn't have time to count
```

I make 132us to be 16,500 clock cycles (at 125MHz) which makes sense as the DMA transfer will take a minimum of 16,384 clock cycles (one cycle per 32-bit chunk), plus some overhead (not least because in dma_channel_configure some stuff is done before the DMA transfer is started).

During 16,500 clock cycles, the CPU counts to 2048.  That's around 8 clock cycles per count.  The assembler the compiler is generating for this counting while loop is, I think:

```
1000037e:       2201            movs    r2, #1
10000380:       4694            mov     ip, r2
10000382:       681a            ldr     r2, [r3, #0]
10000384:       44e1            add     r9, ip
10000386:       420a            tst     r2, r1
10000388:       d1f9            bne.n   1000037e <main+0x76>
```

I make:

* MOVS 1 cycle
* MOV 1 cycle
* LDR 2 cycles
* ADD 1 cycle
* TST 1 cycle
* BNE.n 2 cycles (as branch taken)

So 8 cycles.

## The Code

```
#include <stdio.h>
#include <string.h>
#include "pico/stdlib.h"
#include "hardware/dma.h"

#define COUNT 4*4096
uint32_t src[COUNT];
uint32_t dst[COUNT];

int main() {
    uint64_t time1, time2, time3;
    int ticks;
    dma_channel_config config;

    stdio_init_all();

    // Initialize src data to something
    memset(src, 0, COUNT*sizeof(src[0]));

    while (1)
    {
        // Get a free DMA channel - this function will panic if there are none
        // free
        int chan = dma_claim_unused_channel(true);

        // Do 32-bit transfers, as these are quicker than 8-bit (as 32-bits
        // can be copied in 1 cycle, as opposed to 8)
        config = dma_channel_get_default_config(chan);
        channel_config_set_transfer_data_size(&config, DMA_SIZE_32);
        channel_config_set_read_increment(&config, true);
        channel_config_set_write_increment(&config, true);

        // We'll use ticks for the CPU to count while the DMA transfer takes place
        ticks=0;
        time1=time_us_64();

        // Start the DMA transfer
        dma_channel_configure(chan,
                              &config,
                              dst,
                              src,
                              COUNT,
                              true);

        // While the DMA transfer is taking place, count up
        while (dma_channel_is_busy(chan))
        {
            ticks++;
        }
        time2=time_us_64();

        // Cleanup and free the DMA channel (we should be allocated channel 0
        // again the next time around as nothing else will be allocating DMA
        // channels).
        dma_channel_cleanup(chan);
        dma_channel_unclaim(chan);

        // Print out DMA results
        time3=time2-time1;
        printf("DMA: DMA transfer of %d 32-bit values took %lluus, CPU counted to: %d\n", COUNT, time3, ticks);

        // Now do the equivalent memcpy
        time1=time_us_64();
        memcpy(dst, src, COUNT*sizeof(src[0]));
        time2=time_us_64();
        
        // Print out memcpy results
        time3=time2-time1;
        printf("DMA: memcpy of %d bytes took %lluus, CPU didn't have time to count\n", COUNT*sizeof(src[0]), time3);

        // Pause and then do it again
        sleep_ms(1000);
    }
}
```