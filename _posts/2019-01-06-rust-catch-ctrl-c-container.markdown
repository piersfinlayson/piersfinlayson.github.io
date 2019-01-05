---
layout: post
title:  "Catching Ctrl-C in Rust"
date:   2019-01-06 06:55:00 +0000
categories: rust signal sigint container docker
---

Following on from a [recent post]({% post_url 2019-01-01-rust-signal-handling %}) about signaling handling in Rust, I found that when running my Rust microservices in containers I wasn't able to Ctrl-C these despite running in docker's interactive mode.

Here's some code which allows you to handle this situation gracefully.

Add this to your Cargo.toml's dependencies section:

```
signal-hook = "0.1.7"
```

And this to your program's main.rs:

```
extern crate signal_hook;

pub fn reg_for_sigs() {
    unsafe { signal_hook::register(signal_hook::SIGINT, || on_sigint()) }
        .and_then(|_| {
                debug!("Registered for SIGINT");
                Ok(())
        })
        .or_else(|e| {
            warn!("Failed to register for SIGINT {:?}", e);
            Err(e)
        })
        .ok();
}

fn on_sigint() {
    warn!("SIGINT caught - exiting");
    std::process::exit(128 + signal_hook::SIGINT);
}
```

Then add a call to reg_for_sigs() in your fn main():

```
fn main() {
    ...
    reg_for_sigs()
    ...
}
```

Now when running and you hit Ctrl-C you'll get output like the following when hitting Ctrl-C, and the process will exit.

```
[2019-01-05T13:48:01Z WARN  myApp] SIGINT caught - exiting
```

Note that the reg_for_sigs() method deliberately swallows and logs any error, rather than leaving it for main() to handle.  If you want to see the logs, you'll need to use the [log crate](https://crates.io/crates/log).
