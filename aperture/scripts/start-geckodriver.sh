#!/bin/bash

cd /opt/grub-2.0/aperture/

screen -dmS geckodriver4 bash -c "./geckodriver -v --marionette-port 2928 -p 4444"
screen -dmS geckodriver5 bash -c "./geckodriver -v --marionette-port 2929 -p 4445"
screen -dmS geckodriver6 bash -c "./geckodriver -v --marionette-port 2930 -p 4446"
screen -dmS geckodriver7 bash -c "./geckodriver -v --marionette-port 2931 -p 4447"
screen -dmS geckodriver8 bash -c "./geckodriver -v --marionette-port 2932 -p 4448"
