#!/bin/bash
TYPE=f1-micro
ZONE=us-west1-c
NEW_UUID=$(LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c 4 ; echo)
NAME=fastener

option=$1
PREEMPTIBLE="--preemptible"
IP="35.212.208.88"
UBUNTU_VERSION="ubuntu-1804-bionic-v20220118"

echo "This instance is preemtible, unless it's started with --prod";
case $option in
    -p|--prod|--production)
    unset PREEMPTIBLE
    IP="--address=35.212.208.88"
    echo "Production mode enabled..."
    echo;
esac

if [ -f secrets.sh ]; then
   source secrets.sh # truly, a travesty
   echo "Here's where I say, hold on a second while we fire things up."
   gcloud compute project-info add-metadata --metadata token=$TOKEN
   echo;
else
   echo "Create 'secrets.sh', put a TOKEN=f00bar statement in it and then rerun this script."
   unset IP;
   echo;
   exit;
fi

gcloud compute firewall-rules create fastener-api --allow tcp:8383

SCRIPT=$(cat <<EOF
#!/bin/bash
sudo su -
apt-get update -y
apt-get install unzip -y
apt-get install build-essential -y
apt-get install python-dev -y
apt-get install python-setuptools -y
apt-get install python-paste -y
apt-get install python-pip -y

pip install bottle
pip install google-cloud
pip install --upgrade google-api-python-client
pip install --upgrade pyasn1-modules
pip install google-auth-httplib2

apt-get update

cd /
git clone https://github.com/kordless/grub-2.0
cd /grub-2.0/fastener/
touch RUN_START_WEB

EOF
)

gcloud compute instances create $NAME-$NEW_UUID \
--machine-type $TYPE \
--image "$UBUNTU_VERSION" \
--image-project "ubuntu-os-cloud" \
--boot-disk-size "10GB" \
--boot-disk-type "pd-ssd" \
--boot-disk-device-name "$NEW_UUID" \
--service-account mitta-us@appspot.gserviceaccount.com \
--scopes https://www.googleapis.com/auth/cloud-platform \
--scopes https://www.googleapis.com/auth/compute \
--zone $ZONE \
--labels type=fastener \
--tags mitta,fastener,token-$TOKEN \
$PREEMPTIBLE \
--subnet=default $IP --network-tier=STANDARD \
--metadata startup-script="$SCRIPT"
sleep 15

IP=$(gcloud compute instances describe $NAME-$NEW_UUID --zone $ZONE  | grep natIP | cut -d: -f2 | sed 's/^[ \t]*//;s/[ \t]*$//')

echo "Server started with $IP. Use the SSH button to login."
