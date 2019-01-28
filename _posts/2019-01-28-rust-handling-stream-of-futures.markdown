---
layout: post
title:  "Handling a Stream of Rust Futures"
date:   2019-01-28 17:00:00 +0000
categories: rust futures stream
---

While building RESTful HTTP microservices for Rust, I've had to become quite familiar with the Rust [futures library](https://docs.rs/futures/0.2.1/futures/).  It's taken a lot of getting my head around - the key concept in futures is that you don't know when your code is actually going to execute, and it may execute in small incremental, non-blocking steps - hence you can't and don't handle returns from Futures in the "present", because they don't exist in the context you're writing your code.  This leads to a lot of function chaining, where you write closures (or functions) which map from one return type (from a future) to another and just let the futures library actually run it all at the right time.  After several months I can just about cope with that.

What I've more recently had to do is chain together an arbitrary number of future calls, to build up a single return object - I'm doing this to expose an API which itself needs to call another API repeatedly - i.e. to the save the user from having to do that.  This is more complicated, but can be done with [futures::stream](https://docs.rs/futures/0.1.14/futures/stream/index.html).  From the docs:

```
A stream here is a sequential sequence of values which may take some amount of time in between to produce.
```

Sounds promising.

There's even a helpful [stackoverflow example](https://stackoverflow.com/questions/50850309/how-do-i-iterate-over-a-vec-of-functions-returning-futures-in-rust) on how to do this.  Or at least it would be it if compiled.  Here's [my version](https://play.rust-lang.org/?version=stable&mode=debug&edition=2018&gist=592ad6d4e20ce35f921aa278cadad19f) which does compile - and works.  Full credit to [shepmaster](https://stackoverflow.com/users/155423/shepmaster) who nearly got this right!  (It's entirely possible the API has changed since the stackoverflow answer, hence the reason the example doesn't compile and run.)

```
extern crate futures;

use futures::{future::{self}, stream, Future, Stream};

fn network_request(val: i32) -> impl Future<Item = i32, Error = ()> {        
    // Just for demonstration, don't do this in a real program
    use std::{thread, time::{Duration, Instant}};
    thread::sleep(Duration::from_secs(1));
    println!("Resolving {} at {:?}", val, Instant::now());

    future::ok(val * 100)
}

fn requests_in_sequence(vals: Vec<i32>) -> impl Stream<Item = i32, Error = ()> {
    stream::unfold(vals.into_iter(), |mut vals| {
        match vals.next() {
            Some(v) => Some(network_request(v).map(|v| (v, vals))),
            None => None,
        }
    })
}

fn main() {
    let s = requests_in_sequence(vec![1, 2, 3]);
    println!("Evaluate s");
    let s = s.wait();
    println!("Print out s");
    for s in s {
        println!("-> {:?}", s);
    };
}
```