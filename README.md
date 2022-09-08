# Grub-2.0 
Grub is a system for crawling and indexing documents.

This is a work in progress. Feel free to open tickets.

# Deploy a Solr Neural Indexer on Google Cloud
Useful information and scripts for deploying a Solr indexer hosted on a single machine. 

There is also a [Docker version of Solr available](https://hub.docker.com/_/solr).

## Create a secrets.sh file

```
$ vi secrets.sh
TOKEN=f00bar
:x
```


```
$ ./deploy-solr.sh
```

Instance will be running in 2.5 minutes, listening on port 8389.

URL goes like: http://solr:password@x.x.x.x:8389


## Fastener
Deploy a controller box for Solr instances. The scripts should be copied to Google Compute instance templates.

```
$ ./deploy-fastener.sh
```

Instance will be running and listening on port 80.

## Bookmark and Index
[Bookmark and index](https://mitta.us/https://github.com/kordless/mitta-deploy/) this page using [Mitta.us](https://mitta.us/https://github.com/kordless/mitta-deploy/).
