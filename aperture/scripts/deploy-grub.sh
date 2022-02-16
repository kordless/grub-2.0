#!/bin/bash
TYPE=e2-medium
ZONE=us-west1-c
NAME=grub
NEW_UUID=$(LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c 4 ; echo)

option=$1
PREEMPTIBLE="--preemptible"
# IP="--address=34.82.44.60"

echo "This instance is preemtible, unless it's started with --prod";
case $option in
    -p|--prod|--production)
    unset PREEMPTIBLE
	echo "Production mode enabled..."
    echo;
    IP=""
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
--image "ubuntu-1804-bionic-v20201211a" \
--image-project "ubuntu-os-cloud" \
--boot-disk-size "10GB" \
--boot-disk-type "pd-ssd" \
--boot-disk-device-name "$NEW_UUID" \
--service-account mitta-us@appspot.gserviceaccount.com \
--zone $ZONE \
--labels type=grub \
--tags mitta,grub,token-$TOKEN,bid-$NEW_UUID \
$PREEMPTIBLE \
--subnet=default $IP --network-tier=PREMIUM \
--metadata startup-script='#! /bin/bash
if [ -d "/opt/grub-2.0/" ]; then
  echo "starting grub"
  cd /opt/grub-2.0/aperture
  screen -dmS geckodriver bash -c "bash ./scripts/start-geckodriver.sh"
  screen -dmS grub bash -c "bash ./scripts/start-grub.sh"
else
  sudo su -
  date >> /opt/grub-2.0/apeture/start.time
  apt-get update -y
  apt-get install unzip -y
  apt-get update -y
  apt-get install python3-pip -y

  add-apt-repository ppa:mozillateam/ppa -y
  apt-get update -y
  apt-get install -y --no-install-recommends wget firefox-esr

  ln -s /usr/bin/python3 /usr/bin/python

  pip3 install flask
  pip3 install urllib3
  pip3 install httplib2
  pip3 install requests
  pip3 install gunicorn

  cd /opt/
  git clone https://github.com/kordless/grub-2.0.git

  mkdir /opt/temp
  cd /opt/temp/

  curl https://storage.googleapis.com/mitta-config/geckodriver-v0.28.0-linux64.tar.gz > geckodriver.tar.gz
  tar xzhf geckodriver.tar.gz

  mv geckodriver /opt/grub-2.0/aperture
  cd /opt/grub-2.0
  chmod -R 755 *.sh

  apt-get install apache2-utils -y
  apt-get install nginx -y
  
  cd /opt/grub-2.0/aperture/
  cp nginx.conf.grub /etc/nginx/nginx.conf

  python3 get_token.py grub

  source bidntoken
  echo $TOKEN >> /root/token

  systemctl restart nginx.service
 
  echo "starting grub"
  cd /opt/grub-2.0/aperture/
  bash ./scripts/start-geckodriver.sh
  screen -dmS grub bash -c "bash ./scripts/start-grub.sh"

  date >> /opt/done.time
fi
'
sleep 15

gcloud compute instances add-metadata $NAME-$NEW_UUID --zone $ZONE --metadata-from-file=shutdown-script=stop-grub.sh

IP=$(gcloud compute instances describe $NAME-$NEW_UUID --zone $ZONE  | grep natIP | cut -d: -f2 | sed 's/^[ \t]*//;s/[ \t]*$//')
gcloud compute firewall-rules create grub-proxy --target-tags grub --allow tcp:8983
echo "Password token is: $TOKEN"