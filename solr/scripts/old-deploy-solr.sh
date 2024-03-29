#!/bin/bash
TYPE=n1-standard-4
ZONE=us-west1-c
NAME=solr
VERSION=8.9.0
NEW_UUID=$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 4 | head -n 1)

option=$1
PREEMPTIBLE="--preemptible"
IP="--address=35.230.108.84"

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
--image "ubuntu-1804-bionic-v20201211a" \
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
--metadata startup-script='#!/bin/bash
if [ -d "/opt/solr/" ]; then
  echo "starting solr"
  sudo -i -u solr /opt/solr/bin/solr start
else
  sudo su -
  date >> /opt/start.time
  apt-get update -y
  apt-get install unzip -y
  # install OpenJDK
  apt-get update -y

  #entropy
  apt-get -y install rng-tools
  cat "HRNGDEVICE=/dev/urandom" >> /etc/default/rng-tools
  /etc/init.d/rng-tools restart

  # files
  echo "solr hard nofile 65535" >> /etc/security/limits.conf
  echo "solr soft nofile 65535" >> /etc/security/limits.conf
  echo "solr hard nproc 65535" >> /etc/security/limits.conf
  echo "solr soft nproc 65535" >> /etc/security/limits.conf

  apt-get install openjdk-11-jdk -y
  echo JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64" >> /etc/environment

  cd /opt/

  curl https://archive.apache.org/dist/lucene/solr/8.9.0/solr-8.9.0.tgz > solr-8.9.0.tgz
  tar xzf solr-8.9.0.tgz solr-8.9.0/bin/install_solr_service.sh --strip-components=2

  bash ./install_solr_service.sh solr-8.9.0.tgz -u solr -s solr -p 8983

  cp -rp /opt/solr/server/solr/configsets /var/solr/data/

  chown -R solr.solr /opt/solr*
  chown -R solr.solr /var/solr*

  cd /opt/
  git clone https://github.com/kordless/grub-2.0.git

  cd grub-2.0
  chmod -R 755 *.sh
  ./solr-scripts/start-solr.sh

  cp solr /etc/init.d/solr
  chmod 755 /etc/init.d/solr

  apt-get install apache2-utils -y
  apt-get install nginx -y
  cp nginx.conf.solr /etc/nginx/nginx.conf

  python3 get_token.py solr

  systemctl restart nginx.service

  date >> /opt/done.time

fi
'
sleep 15

gcloud compute instances add-metadata $NAME-$NEW_UUID --zone $ZONE --metadata-from-file=shutdown-script=stop-solr.sh

IP=$(gcloud compute instances describe $NAME-$NEW_UUID --zone $ZONE  | grep natIP | cut -d: -f2 | sed 's/^[ \t]*//;s/[ \t]*$//')
gcloud compute firewall-rules create solr-proxy --target-tags solr --allow tcp:8389
echo "Password token is: $TOKEN"