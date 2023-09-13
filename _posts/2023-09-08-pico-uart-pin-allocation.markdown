---
layout: post
title:  "Pico UART GPIO allocation"
date:   2023-09-08 7:01 +0000
tags:   raspberry pi pico sdk picotool bare metal gpio pin
---

The Raspberry Pi Pico supports two UARTs, UART0 and UART1.  The RX and TX pins used for each UART is configurable, and this is documented in [Table 278 General Purpose Input/Output (GPIO) User Bank Functions](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf):

|  UART    | Option 1 | Option 2 | Option 3 | Option 4 |
|:--------:|:--------:|:--------:|:--------:|:--------:|
| UART0 TX |  GP0  |  GP12  |  GP16  |  GP28  |
| UART0 RX |  GP1  |  GP13  |  GP17  |  GP29  |
| UART1 TX |  GP4  |  GP8   |  GP20  |  GP24  |
| UART1 RX |  GP5  |  GP9   |  GP21  |  GP25  |

Likewise UART CTS and RTS (if needed/used) can also be assigned to 4 different pin options.

To set the appropriate pin via the C SDK, one uses the _gpio_set_function_ function.  Here's the function call:

```
void gpio_set_function (uint gpio, enum gpio_function fn)
```

To set pin 0 to UART (and by implication UART0 TX) use:

```
gpio_set_function(0, GPIO_FUNC_UART);
```

To set pin 21 to UART (by definition UART1 RX) use:

```
gpio_set_function(21, GPIO_FUNC_UART);
```

What happens if you set more than one pin for the same UART TX or RX?  According to the [RP2040 datasheet](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf) (which says you shouldn't do this), for TX lines the signal output is a logical OR of the combined pins.  Presumably (although this is not stated by the datasheet), the same is true for the a UART RX connected to multiple GPIOs simultaneously.

As described [here](drive-two-uarts-on-the-pico-one-usb-serial.html) you can also configure the USB serial interface (which is handy for logging), to use either UART0 or UART1.  To do so, add this to your CMakeLists.txt:

```
add_definitions(-DPICO_DEFAULT_UART=1
  -DPICO_DEFAULT_UART_TX_PIN=4
  -DPICO_DEFAULT_UART_RX_PIN=5
)
pico_enable_stdio_usb(uarts 1)
```

The _PICO_DEFAULT_UART_TX_PIN_ and _PICO_DEFAULT_UART_TX_PIN_ #defines may be unnecessary here, as UART1 defaults to pins 4/5.

Finally, when configuring non-default options for your UART, it may be a good idea to add binary information to your image, indicating this has been done.  For example, in your main.c, you could add this to indicate that UART1 is using 24/25 for TX/RX:

```
bi_decl(bi_2pins_with_func(24, 25, GPIO_FUNC_UART));
```