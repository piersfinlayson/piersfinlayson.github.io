---
layout: post
title:  "Rust Signal Handling (to reload config)"
date:   2019-01-01 08:12:00 +0000
categories: rust signal nix unix sighup hup config reload
---

As I said in a previous post, I'm planning to run a bunch of Rust based microservices in minimal docker containers.  One of the functions I want is the ability to update the configuration of those microservices dynamically, and the typical unixy way of doing this is by sending the process a SIGHUP (that's a hangup signal).  With docker we'd do this:

```
docker kill -s HUP <container name or id>
```

Note that this isn't terribly reliable unless the process you're sending to is PID 1 in the container (which it would be in a properly minimal container).  Otherwise you can use

```
kill -HUP <host process id of app within the container>
```

I knocked together the following sample Rust app to prototype this function.

```
extern crate signal_hook;

use std::io::Error;

static mut CONFIG: i32 = 0;

// Rgisters for SIGHUP - on receipt of SIGHUP on_hup() will be called
fn register_hup() -> Result<(), Error> {
    let _hup = unsafe {
        signal_hook::register(signal_hook::SIGHUP, || on_hup())
    }?;
    Ok(())
}

// Triggers program to reload config - this is a poor way of doing this
// Should send a signal to the main thread
fn on_hup() {
    println!("Reloading config");
    unsafe { CONFIG += 1 };
}

fn get_config() -> i32 {
    unsafe { CONFIG }
}

fn main() -> Result<(), Error> {
    register_hup()?;

    // Check if config has changdd
    // Ahain, nbot a good way of doing this
    let mut config = get_config();
    let mut old_config = config;
    loop {
        if config != old_config {
            println!("Config changed: {}", config);
            old_config = config;
        }
        config = get_config();
    }
}
```