# Grub-2.0 
Grub is a set of deployment scripts and programs for Google Cloud which creates an AI system for crawling and indexing documents or URLs.

This is a work in progress.

# Deploy Solr on Google Cloud
Useful information and scripts for deploying an instance based Solr Cloud in 2 minutes.

Check this repo out on your Google Cloud Shell terminal.

## Launch Solr
Deploy a secure Solr instance on Google cloud:

```
$ ./deploy-solr.sh
Password token is: f00bar
```

### Create a secrets.sh file

```
$ vi secrets.sh
TOKEN=f00bar
:x
```

Instance will be running in 2.5 minutes, listening on port 8389.

URL like: http://solr:password@x.x.x.x:8389

## Fastener
Deploy a controller box for Solr instances. Not done yet.

```
$ ./deploy-fastener.sh
```

Instance will be running and listening on port 80.

## Bookmark and Index
[Bookmark and index](https://mitta.us/https://github.com/kordless/mitta-deploy/) this page using [Mitta.us](https://mitta.us/https://github.com/kordless/mitta-deploy/).
