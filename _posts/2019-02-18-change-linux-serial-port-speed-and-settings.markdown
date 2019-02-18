---
layout: post
title:  "Changing serial port speed and settings in Linux"
date:   2019-02-18 17:32:00 +0000
categories: serial linux uart port speed EINVAL PARENB
---

This post contains a sample C program to change Linux serial port speed and other settings.  In particular setting parity transmit and receive checking (PARENB), which was failing on a Raspberry Pi ZeroW serial port, until I figured out how to use the PL011 UART instead of the mini UART.  See [this post]({% post_url 2019-02-18-raspberry-pi-serial-ports %}) for more details on BCM28350-based Raspberry Pis.

To compile this program:

```
gcc serial.c -o serial
```

To run:

```
./serial /dev/serial0  # Or another device
````

The source code:

```
//
// (C) Piers Finlayson 2019
//
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program.  If not, see <https://www.gnu.org/licenses/>.
//

#include <fcntl.h>
#include <stdio.h>
#include <termios.h>
#include <errno.h>

#define DEVICE "/dev/serial0"

struct baud_rate
{
  speed_t baud;
  char *bauds;
};

#define NUM_BAUD_RATES 16
struct baud_rate rates[NUM_BAUD_RATES] =
{
  {B0, "0"},
  {B50, "50"},
  {B75, "75"},
  {B110, "110"},
  {B134, "134"},
  {B150, "150"},
  {B200, "200"},
  {B300, "300"},
  {B600, "600"},
  {B1200, "1200"},
  {B1800, "1800"},
  {B2400, "2400"},
  {B4800, "4800"},
  {B9600, "9600"},
  {B19200, "19200"},
  {B38400, "38400"},
};

char *get_baud_rate_as_string(speed_t speed)
{
  int ii;
  char *speeds = "unknown";

  for (ii = 0; ii < NUM_BAUD_RATES; ii++)
  {
    if (rates[ii].baud == speed)
    {
      speeds = rates[ii].bauds;
      break;
    }
  }

  return speeds;
}

int get_termios(int fd, struct termios *t)
{
  int rc;
  rc = tcgetattr(fd, t);
  return rc;
}

void change_termios(struct termios *t)
{
  t->c_cflag |= CS8 | CREAD | CLOCAL | PARENB;
  t->c_cc[VMIN] = (cc_t)0;
  t->c_cc[VTIME] = (cc_t)2;
}

int set_termios(int fd, struct termios *t)
{
  int rc;
  rc = tcsetattr(fd, TCSANOW, t);
  return rc;
}

void log_termios(struct termios *t)
{
  int ii;

  fprintf(stdout, "  c_iflag 0x%08x\n", t->c_iflag);
  fprintf(stdout, "  c_oflag 0x%08x\n", t->c_oflag);
  fprintf(stdout, "  c_cflag 0x%08x\n", t->c_cflag);
  fprintf(stdout, "  c_lflag 0x%08x\n", t->c_lflag);
  for (ii = 0; ii < NCCS; ii++)
  {
    fprintf(stdout, "c_cc[%d} 0x%08x\n", ii, t->c_cc[ii]);
  }

  return;
}

int open_device(char *dev)
{
  int fd;
  fd = open(dev, O_RDWR | O_NOCTTY);
  return fd;
}

int set_ospeed(struct termios *t, speed_t speed)
{
  int rc;
  rc = cfsetospeed(t, speed);
  return rc;
}

int set_ispeed(struct termios *t, speed_t speed)
{
  int rc;
  rc = cfsetispeed(t, speed);
  return rc;
}

speed_t get_ospeed(struct termios *t)
{
  speed_t rc;
  rc = cfgetospeed(t);
  return rc;
}

speed_t get_ispeed(struct termios *t)
{
  speed_t rc;
  rc = cfgetispeed(t);
  return rc;
}

#define EXIT_IF_FAILED(X, ...)     \
if (X < 0)                         \
{                                  \
  fprintf(stderr, ##__VA_ARGS__);  \
  return -1;                       \
}

int main(int argc, char *argv[])
{
  struct termios t;
  int fd, rc;
  char *device;
  speed_t speed;

  if (argc > 1)
  {
    device = argv[1];
  }
  else
  {
    device = DEVICE;
  }

  fprintf(stdout, "Using device %s\n", device);

  fd = open_device(device);
  EXIT_IF_FAILED(fd, "Failed to open device %s %d\n", device, errno);

  change_termios(&t);
  rc = get_termios(fd, &t);
  EXIT_IF_FAILED(fd, "Failed to open device %s %d\n", device, errno);
  log_termios(&t);

  rc = set_ispeed(&t, B2400);
  EXIT_IF_FAILED(rc, "Failed to set ispeed %d\n", errno);

  rc = set_ospeed(&t, B2400);
  EXIT_IF_FAILED(rc, "Failed to set ospeed %d\n", errno);

  rc = set_termios(fd, &t);
  EXIT_IF_FAILED(rc, "Failed to set termios %d\n", errno);

  speed = get_ispeed(&t);
  fprintf(stdout, "  ispeed set to %s baud\n", get_baud_rate_as_string(speed));

  speed = get_ospeed(&t);
  fprintf(stdout, "  ospeed set to %s baud\n", get_baud_rate_as_string(speed));

  return 0;
}
```