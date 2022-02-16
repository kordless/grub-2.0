#!/bin/bash
cd /opt/grub-2.0/aperture/
./geckodriver -v --marionette-port 2928 -p 4444 &
./geckodriver -v --marionette-port 2929 -p 4445 &
./geckodriver -v --marionette-port 2930 -p 4446 &
./geckodriver -v --marionette-port 2931 -p 4447 &
./geckodriver -v --marionette-port 2932 -p 4448 &