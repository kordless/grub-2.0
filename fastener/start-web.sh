#!/bin/bash

mkdir -v keys
export GOOGLE_APPLICATION_CREDENTIALS="/grub-2.0/mitta-us.json"
screen -dmS buttons bash -c "bash do-web.sh"
