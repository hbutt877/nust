#!/bin/sh

while true; do
    pkill python;
    pkill chrome;
    timeout 200 python3 login.py;
done
