#!/bin/bash

while true; do
  cd /opt/grub-2.0/aperture/
  gunicorn -w 8 -b 0.0.0.0:7070 grub:app
  sleep 5
done

