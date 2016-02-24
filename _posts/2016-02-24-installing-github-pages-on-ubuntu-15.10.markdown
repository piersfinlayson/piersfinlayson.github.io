---
layout: post
title:  "Installing Github Pages on Ubuntu 15.10"
date:   2016-02-24 19:44:59 +0000
categories: jekyll ruby ubuntu github
---
# Simples

Why oh why do people make everything as hard as possible?  I wanted to create a blog using github pages, but despite looking in all the obvious places I couldn't find a simple set of instructions _all in one place_ that explained how to do this.

Sigh.  Cue neverending redirect from one site to another saying I needed to do this, that or the other first.  This would probably be easy if I used ruby and had it and rubygems already installed, but it's been years since I've done anything with it.

I use Ubuntu as my distro of choice and started out from a vanilla Ubuntu (an OpenSSH server install).

# Github Pages

[Github Pages](https://pages.github.com/) uses [jekyll](https://jekyllrb.com/).  To use jekyll you need [ruby](https://www.ruby-lang.org/en/downloads/).  I had tried the apt-get route before and had problems, so decided to build form source.

# Install Ruby From Source

Here's how to do that:

    sudo apt-get -y install build-essential zlib1g-dev libssl-dev libreadline6-dev libyaml-dev
    wget https://cache.ruby-lang.org/pub/ruby/2.3/ruby-2.3.0.tar.gz
    tar zxvf ruby-2.3.0.tar.gz
    cd ruby-2.3.0/
    make
    sudo make install
    cd ..
    ruby --version

Check the output is 2.3.0:

    ruby 2.3.0p0 (2015-12-25 revision 53290) [x86_64-linux]

# RubyGems

Again, from source:

    sudo apt-get install git
    git clone https://github.com/rubygems/rubygems.git
    cd rubygems/
    ruby setup.py #

# Github Pages

Now it's easy

    get install github-pages

# Creating Github Pages Site

This was easy - I had already created a github repo _piersfinlayson.github.io_.  Here's how I created the jekyll site (obviously change all the piersfinlayson stuff to your own github account and pages site):

    git clone https://github.com/piersfinlayson/piersfinlayson.github.io
    cd piersfinlayson.github.io
    jekyll new .

Next I edited _config.yml and about.md entering the info about my site.

# First Post

Finally I did:

    cd _posts

And then modified the sample post already there and turned it into this one.

# Running jekyll

The usual instructions tell you how to run jekyll to serve pages up on localhost.  Not much good to me with a headless virtual Ubuntu instance.  So here's how to expose externally:

    cd ..  # Back to ~/piersfinalayson.github.io
    jekyll -serve --host 0.0.0.0

Job's a goodun.  All that's left is to push this to github and it should be visible  [publicly](https://piersfinlayson.github.io/).
