#!/bin/bash
TYPE=n1-standard-4
ZONE=us-west1-c
NAME=solr
VERSION=8.6.3
NEW_UUID=$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 4 | head -n 1)

option=$1
PREEMPTIBLE="--preemptible"
IP="--address=35.233.155.193"

echo "This instance is preemtible, unless it's started with --prod";
case $option in
    -p|--prod|--production)
    unset PREEMPTIBLE
	echo "Production mode enabled..."
    echo;
esac

if [ -f secrets.sh ]; then
   source secrets.sh # truly, a travesty, sets TOKEN=token-[passphrase]
   echo "Here's where I say, hold on a second while we fire things up."
   gcloud compute project-info add-metadata --metadata token=$TOKEN
   echo;
else
   echo "Create 'secrets.sh', put a TOKEN=f00bar statement in it and then rerun this script."
   echo;
   exit;
fi

gcloud compute instances create $NAME-$NEW_UUID \
--machine-type $TYPE \
--image "ubuntu-1804-bionic-v20201116" \
--image-project "ubuntu-os-cloud" \
--boot-disk-size "10GB" \
--boot-disk-type "pd-ssd" \
--boot-disk-device-name "$NEW_UUID" \
--service-account mitta-us@appspot.gserviceaccount.com \
--zone $ZONE \
--labels type=solr \
--tags mitta,solr,token-$TOKEN \
--preemptible \
--subnet=default $IP --network-tier=PREMIUM \
--metadata startup-script='#! /bin/bash
if [ -d "/opt/mitta-deploy/" ]; then
  echo "starting grub"
  bash /opt/mitta-deploy/grub-scripts/start-grub.sh
else
  sudo su -
  date >> /opt/start.time
  apt-get update -y
  apt-get install unzip -y
  apt-get update -y

  cd /opt/
  
  curl https://storage.googleapis.com/mitta-config/geckodriver-v0.28.0-linux64.tar.gz > geckodriver.tar.gz
  tar xzf geckodriver.tar.gz

  git clone https://github.com/kordless/mitta-deploy.git

  mv geckodriver /opt/mitta-deploy/

  cd mitta-deploy
  
  chmod -R 755 *.sh
  ./grub-scripts/start-grub.sh

  date >> /opt/done.time

fi
'
sleep 15
IP=$(gcloud compute instances describe $NAME-$NEW_UUID --zone $ZONE  | grep natIP | cut -d: -f2 | sed 's/^[ \t]*//;s/[ \t]*$//')
gcloud compute firewall-rules create solr-proxy --allow tcp:8389
echo "Password token is: $TOKEN"
histo