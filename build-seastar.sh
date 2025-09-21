#!/usr/bin/env bash

sudo git clone https://github.com/scylladb/seastar.git

cd seastar/

sudo ./install-dependencies.sh

sudo ./configure.py --mode=release

ninja -C build/release -j2

sudo ninja -C build/release install
