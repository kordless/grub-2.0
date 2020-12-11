# Grub 2.0
[Grub "one oh"](https://en.wikipedia.org/wiki/Grub_(search_engine)) was an Open Source search engine designed to distribute the job of gathering content (crawling) from the web. Grub was purchased and later resold to Wikimedia. Grub-2.0 is a further expansion on the idea of decentralizing search processes.

Grub-2.0 provides a means of "sight" for a machine, which is talking to a user or another machine learning model. When Grub is given a URL, it may return one or more images and indexes by which images may be queried later using search features such as time or relatedness. 

This may be useful in training machine learning models or providing user level search features.

## How
Queried by URL, Grub "crawls" the page visually using Gekcodriver. An image of the code run during the session is also available.

![foo](https://raw.githubusercontent.com/kordless/grub-2.0/main/docs/index.png)

Grub "looks" at the page like a user would, by imaging it with an "eye". By passing this image to a machine learning model, text found on a page may be converted into data. Another model could find and crop images on the page, which are then extracted and passed to yet another model for more tagging.

Here is Google Vision looking at a Bloomberg article.

![andy](https://raw.githubusercontent.com/kordless/grub-2.0/main/docs/googlevision.PNG)

Grub runs on [Flask](https://flask.palletsprojects.com/en/1.1.x/) in Python and uses [Solr 7.5.2](https://lucene.apache.org/solr/), [Webdriver](https://github.com/SeleniumHQ/selenium) and [Tensorflow](https://github.com/tensorflow/tensorflow).

## Install
This open code repository provides information and scripts for deploying the system.

Begin by checking out this repo onto your Google Cloud Shell terminal:

```
$ git clone https://github.com/kordless/grub-2.0.git
```

![foo](https://github.com/kordless/grub-2.0/blob/main/docs/googlecloud.PNG?raw=true)

## Edit the secrets.sh file:

```
$ cd grub-2.0
$ vi secrets.sh
TOKEN=f00bark
:x
```

Then copy it into script directories:

```
$ cp secrets.sh grub-scripts
$ cp secrets.sh solr-scripts
$ cp secrets.sh tensor-scripts
```

## Deploy Solr
Deploy a secure Solr instance on Google cloud:

```
$ ./deploy-solr.sh
Password token is: f00bark
```

## Deploy Grub
Deploy a secure Grub instance on Google cloud:

```
$ ./deploy-grub.sh
Password token is: f00bark
```

Instances will be running in 2.5 minutes, listening on port 8389 for Solr and 8983 for Grub.

## Manage Solr
Login URL looks like: http://solr:f00bark@x.x.x.x:8389

## Tensorflow
Deploy a tensorflow model. Not done yet.

```
$ ./deploy-tensorflow.sh
Password token is: f00bark
```

## Fastener
Deploy a controller box for starting instances. Not done yet.

```
$ ./deploy-fastener.sh
```

Instance will be running in 2.5 minutes, listening on port 80.

## Bookmark
[Bookmark and index](https://mitta.us/https://github.com/kordless/grub-2.0/) this page using [Mitta.us](https://mitta.us/).
