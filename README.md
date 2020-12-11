# Grub 2.0
Grub is AI applied to crawling the web. When you give Grub a URL, it returns an image and index by which you can query for that image later. This may be useful in training new visual models.

This open code repository provides information and scripts for deploying your own Solr based system onto Google Cloud.

Begin by checking out this repo onto your Google Cloud Shell terminal.

![foo](https://github.com/kordless/grub-2.0/blob/main/docs/googlecloud.PNG?raw=true)


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

Instance will be running in 2.5 minutes, listening on port 80.

## Bookmark and Index
[Bookmark and index](https://mitta.us/https://github.com/kordless/mitta-deploy/) this page using [Mitta.us](https://mitta.us/https://github.com/kordless/mitta-deploy/).
