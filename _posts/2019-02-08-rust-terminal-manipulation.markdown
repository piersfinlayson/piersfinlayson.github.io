---
layout: post
title:  "Terminal manipulation in Rust"
date:   2019-02-08 17:00:00 +0000
categories: rust terminal ansi vt100
---

The program in this post presents two similar approaches for manipulating text within a terminal in Rust - moving around the terminal to overwrite was has been written already.  The two approaches are labelled in the code as direct and indirect:

* The direct approach uses [ANSI VT100](http://www.termsys.demon.co.uk/vtansi.htm) codes directly within print!() statements to move around the terminal.

* The indirect approach uses the [ansi-escapes crate](https://crates.io/crates/ansi-escapes).

In both cases we have to implement the backspace character (which you'd printf with a "\b" in C) ourselves.

```
use ansi_escapes::*;

const ESC: char = 27u8 as char;
const BACKSPACE: char = 8u8 as char;

fn up() -> String {
    format!("{}[A", ESC)
}

fn erase() -> String {
    format!("{}[2K", ESC)
}

fn direct() {
    println!("Hello, world!");
    print!("{}{}", up(), erase());
    print!("Hello, me!");
    print!("{}{}{}", BACKSPACE, BACKSPACE, BACKSPACE);
    println!("everybody!");
}

fn backspace(num: i32) -> String {
    (0..num).map(|_| BACKSPACE).collect()
}

fn indirect() {
    println!("Hello, world!");
    print!("{}{}", CursorUp(1), EraseLine);
    print!("Hello, me!");
    print!("{}", backspace(3));
    println!("everybody!");
}

fn main() {
    direct();
    indirect();
}
```

You'll need this in your Cargo.toml [dependencies] section:

```
ansi-escapes = "0.1.0"
```

The ansi-escapes crate has various other function such as

* Beep
* ClearScreen
* CursorHide.