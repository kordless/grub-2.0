#!/bin/bash

while true; do
  cd /opt/grub-2.0/aperture/
  gunicorn -w 5 -b 127.0.0.1:7070 grub:app
done

