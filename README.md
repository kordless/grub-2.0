# Grub 2.0
[Grub "1.0"](https://en.wikipedia.org/wiki/Grub_(search_engine)) was an Open Source search engine designed to distribute the job of gathering content from the web (crawling). Grub was purchased and later resold to Wikimedia. Grub-2.0 is a further expansion on the idea of decentralizing search processes. We may have to rename it, if the bootloader gods will it.

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Grub.svg/440px-Grub.svg.png" width="200">

Keeping Grubby's huge eyeballs in mind, Grub provides a "computed aperture function" for machines and humans to "see" a website without needing to browse to the site. Many of us can see a taxi in mind when someone says the word *taxi*. The ancients thought people had internal sense organs which "saw" things that were not real.Here's an old sketch of how they thought this worked:

<img src="https://raw.githubusercontent.com/kordless/grub-2.0/main/docs/h2ssme1AjSKfObij3DMZyQ2.jpg" width="300">


Google provides this function, but does so for all data they have crawled. A machine or human using Grub will receive similar imagery using search queries like "robot hand", given the system has been able to view a few pages on robot hands:

<img src="https://i.ytimg.com/vi/l6xqTcLXXC8/h2ssme1AjSKfObij3DMZyQ2.jpg" width="500">

When Grub is given a URL, it may return one or more image and word index. Images may be queried by time or relatedness. 

This may be useful for training machine learning models or providing usercentric search features.

## How
Queried by URL, Grub "crawls" the page visually using Gekcodriver and machine learning models trained to find crops for  images found on a web page.

<img src="https://raw.githubusercontent.com/kordless/grub-2.0/main/docs/index.png" width="500">

Grub "looks" at the page using a computed aperture implemented with Geckodriver, Solr and machine leaarning. By passing a website's images through mutiple model paths, we may find and crop related images on the page. Those new images may be passed onto other models for object extraction, while others may detect and decode text for indexing.

Here we see Google Vision looking at a Bloomberg article and seeing people, given Cuomo is people. A subsequent search, "cuomo people", would return this article and a picture of Cuomo.

<img src="https://raw.githubusercontent.com/kordless/grub-2.0/main/docs/googlevision.PNG" width="500">

Grub runs on [Flask](https://flask.palletsprojects.com/en/1.1.x/) in Python and uses [Solr 7.5.2](https://lucene.apache.org/solr/), [Webdriver](https://github.com/SeleniumHQ/selenium) and [Tensorflow](https://github.com/tensorflow/tensorflow).

## Install
This open code repository provides information and scripts for deploying the system.

Begin by checking out this repo onto your Google Cloud Shell terminal:

```
$ git clone https://github.com/kordless/grub-2.0.git
```

<img src="https://github.com/kordless/grub-2.0/blob/main/docs/googlecloud.PNG?raw=true" width="500">

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

## Credits
*"Your ideas don't stink. Just make sure they become a reality."* - Igor Stojanovski, Grub Developer

Thanks, Igor. I forgot this for a while, but I am "keeping" it clearly in mind now.
