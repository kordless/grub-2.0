#!/bin/bash
TYPE=n1-standard-4
ZONE=us-west1-c
NAME=solr
NEW_UUID=$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 4 | head -n 1)
gcloud compute instances create $NAME-$NEW_UUID \
--machine-type $TYPE \
--image "ubuntu-1804-bionic-v20201014" \
--image-project "ubuntu-os-cloud" \
--boot-disk-size "10" \
--boot-disk-type "pd-ssd" \
--boot-disk-device-name "$NEW_UUID" \
--service-account the-site@appspot.gserviceaccount.com \
--zone $ZONE \
--labels type=solr \
--tags sailsearch \
--preemptible \
--metadata startup-script='#! /bin/bash
sudo su -
apt-get update -y
apt-get install unzip -y
# install OpenJDK
apt-get update -y
apt-get install openjdk-8-jdk -y
echo JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64" >> /etc/environment

'
sleep 15
IP=$(gcloud compute instances describe $NAME-$NEW_UUID --zone $ZONE  | grep natIP | cut -d: -f2 | sed 's/^[ \t]*//;s/[ \t]*$//')
gcloud compute firewall-rules create fusion --allow tcp:8764
gcloud compute firewall-rules create fusion --allow tcp:8763
