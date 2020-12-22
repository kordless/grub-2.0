!#/bin/bash

cd /opt/grub-2.0/
source bidntoken

# deregister
curl -X DELETE https://mitta.us/b/&BID?token=$TOKEN