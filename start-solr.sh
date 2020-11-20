#!/bin/bash
TYPE=n1-standard-4
ZONE=us-west1-c
NAME=solr
VERSION=8.7.0
NEW_UUID=$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 4 | head -n 1)

option=$1
PREEMPTIBLE="--preemptible"
IP="--address=X.X.X.X"

echo "This instance is preemtible, unless it's started with --prod";
case $option in
    -p|--prod|--production)
    unset PREEMPTIBLE
    IP="--address=35.233.156.51"
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
--tags mitta,solr,$TOKEN \
--preemptible \
--metadata startup-script='#! /bin/bash
sudo su -
apt-get update -y
apt-get install unzip -y
# install OpenJDK
apt-get update -y

# java
apt-get install openjdk-11-jdk -y
echo JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64" >> /etc/environment

# work here
cd /opt/

# grab solr and extract installer
curl https://archive.apache.org/dist/lucene/solr/8.7.0/solr-8.7.0.tgz > solr-8.7.0.tgz
tar xzf solr-8.7.0.tgz solr-8.7.0/bin/install_solr_service.sh --strip-components=2

# run installer
bash ./install_solr_service.sh solr-8.7.0.tgz -u solr -s solr -p 8983

# update perms
mkdir /opt/solr/server/logs/
cd /opt/
chown -R solr.solr solr*

# fix up a config for nginx
git clone https://github.com/kordless/mitta-deploy.git
cd mitta-deploy

# install nginx
apt-get install apache2-utils
apt-get install nginx -y
cp nginx.conf /etc/nginx/

# set password
htpasswd -b -c /etc/nginx/htpasswd solr $TOKEN

# expose 8389 --> solr 8983
systemctl restart nginx.service

'
sleep 15
IP=$(gcloud compute instances describe $NAME-$NEW_UUID --zone $ZONE  | grep natIP | cut -d: -f2 | sed 's/^[ \t]*//;s/[ \t]*$//')
gcloud compute firewall-rules create solr-proxy --allow tcp:8389
echo "Password token is: $TOKEN"