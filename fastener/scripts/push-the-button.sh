#!/bin/bash

# Temporary script until Kord does his magic

# World, the time has come to...

if [ -z "$1" ]; then
  echo "What button do you want to push?   'push-the-button.sh <button ID>'" >&2
  exit 1
fi

SID="$1"

# TODO: should we check that IID doesn't already exist and loop until we get a new one?
IID=$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 4 | head -n 1)
ZONE=us-west1-c

gcloud compute instances create button-$SID-$IID \
--machine-type "n1-standard-4" \
--image "ubuntu-1604-xenial-v20180627" \
--image-project "ubuntu-os-cloud" \
--boot-disk-size "200" \
--boot-disk-type "pd-ssd" \
--boot-disk-device-name "$IID" \
--zone $ZONE \
--labels type=button,sid=$SID,iid=$IID \
--tags fusion \
$PROD \
--metadata-from-file startup-script=bin/start-button.sh

sleep 15

IP=$(gcloud compute instances describe button-$SID-$IID --zone $ZONE  | grep natIP | cut -d: -f2 | sed 's/^[ \t]*//;s/[ \t]*$//')
gcloud compute firewall-rules create fusion --allow tcp:8764
gcloud compute firewall-rules create fusion --allow tcp:8763
gcloud compute firewall-rules create fusion-appkit --allow tcp:8080
gcloud compute firewall-rules create fusion-webapp --allow tcp:8780
gcloud compute firewall-rules create fusion-webapp --allow tcp:9999

echo "Button $SID pushed and launched"
echo "Fusion UI available in a few minutes at: http://$IP:8764"
