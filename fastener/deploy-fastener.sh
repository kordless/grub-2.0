#!/bin/bash

NEW_UUID=$(cat /dev/urandom | env LC_CTYPE=C tr -dc 'a-z0-9' | fold -w 4 | head -n 1)
ZONE=us-west2-c
NAME=fastener-api

option=$1
PREEMPTIBLE="--preemptible"
IP="--address=X.X.X.X"

echo "This instance is preemtible, unless it's started with --prod";
case $option in
    -p|--prod|--production)
    unset PREEMPTIBLE
    IP="--address=35.230.26.45" #fastener.lucidworks.com
    echo "Production mode enabled..."
    echo;
    unset IP;
esac

if [ -f secrets.sh ]; then
   source secrets.sh # truly, a travesty
   echo "Here's where I say, hold on a second while we fire things up."
   gcloud compute project-info add-metadata --metadata token=$TOKEN
   echo;
else
   echo "Create 'secrets.sh', put a TOKEN=f00bar statement in it and then rerun this script."
   echo;
   exit;
fi

#gcloud compute instances attach-disk $NAME-$NEW_UUID --disk $NAME-data --zone $ZONE
gcloud compute firewall-rules create fastener-api --allow tcp:80,tcp:8091,tcp:8764,tcp:8765,tcp:8766,tcp:8769,tcp:8984,tcp:8983,tcp:9983,tcp:8766,tcp:8780,tcp:8767,tcp:8082,tcp:8770,tcp:4040,tcp:8769,tcp:7337,tcp:8600-8616,tcp:47100-48099,tcp:48100-48199,tcp:49200-49299,tcp:51500-52000

gcloud beta compute instances create $NAME-$NEW_UUID \
--machine-type "n1-standard-2" \
--image "ubuntu-1604-xenial-v20180627" \
--image-project "ubuntu-os-cloud" \
--boot-disk-size "50" \
--boot-disk-type "pd-ssd" \
--boot-disk-device-name "$NAME-disk-$NEW_UUID" \
--zone $ZONE \
--tags http-server,lucid,token-$TOKEN \
--scopes compute-rw, https://www.googleapis.com/auth/cloud-platform \
--subnet=default $IP --network-tier=PREMIUM \
--service-account labs-209320@appspot.gserviceaccount.com \
$PREEMPTIBLE \
--metadata startup-script='#! /bin/bash
sudo su -

apt-get update -y
apt-get install unzip -y
apt-get install build-essential -y
apt-get install python-dev -y
apt-get install python-setuptools -y
apt-get install python-paste -y
easy_install pip
pip install bottle
pip install google-cloud
pip install --upgrade google-api-python-client
pip install --upgrade pyasn1-modules
pip install google-auth-httplib2

curl -L https://git.io/get_helm.sh | bash
helm init

apt-get update && apt-get install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | tee -a /etc/apt/sources.list.d/kubernetes.list
apt-get update
apt-get install -y kubectl

#upgrade SSL
sudo mkdir /usr/local/share/ca-certificates/cacert.org
sudo wget -P /usr/local/share/ca-certificates/cacert.org http://www.cacert.org/certs/root.crt http://www.cacert.org/certs/class3.crt
sudo update-ca-certificates

gcloud beta container clusters get-credentials lucidworks-streams-fusion5-cluster --region us-central1 --project labs-209320

cd /;
git clone https://github.com/lucidworks/streams.git
cd /streams/projects/buttons/fastener/;
screen -dmS buttons bash -c "bash start-web.sh"
'

sleep 20
IP=$(gcloud compute instances describe $NAME-$NEW_UUID --zone $ZONE  | grep natIP | cut -d: -f2 | sed 's/^[ \t]*//;s/[ \t]*$//')

echo "Server started with $IP. Use the SSH button to login."
echo "Try http://$IP"
