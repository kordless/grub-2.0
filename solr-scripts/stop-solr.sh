#!/bin/bash
sudo -i -u solr /opt/solr/bin/solr stop -c -p 8983
echo "shutdown complete" >> /root/solr-shutdown.log