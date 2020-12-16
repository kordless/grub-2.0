# Grub 2.0
[Grub "one oh"](https://en.wikipedia.org/wiki/Grub_(search_engine)) was an Open Source search engine designed to distribute the job of gathering content from the web (crawling). Grub was purchased and later resold to Wikimedia. Grub-2.0 is a further expansion on the idea of decentralizing search processes.

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Grub.svg/440px-Grub.svg.png" width="200">

Likey Grubby's huge eyeballs, Grub-2.0 provides a mental eye, or *"seeing things in mind"* function for machines or humans. Many of us see a taxi (in mind) when someone says the word *taxi*, all usually without having to have a real taxi on hand. 

<img src="https://upload.wikimedia.org/wikipedia/commons/0/0c/RobertFuddBewusstsein17Jh.png" width="300">


Similar to what Google provides for all data, a machine or human using Grub will receive related imagery by using optimized search queries like "robot hand", given the system had been shown some pages on robot hands:

<img src="https://i.ytimg.com/vi/l6xqTcLXXC8/maxresdefault.jpg" width="500">

When Grub is given a URL, it may return one or more image and word index. Images may be queried by time or relatedness. 

This may be useful for training machine learning models or providing usercentric search features.

## How
Queried by URL, Grub "crawls" the page visually using Gekcodriver. An image of the code run during the session is also available.


<img src="https://raw.githubusercontent.com/kordless/grub-2.0/main/docs/index.png" width="500">

Grub "looks" at the page like a user would, by imaging it with an "eye" which, in part, looks like Geckodriver-->Multiple Machine Models-->Solr. By passing this image through mutiple models one model can find and crop images on the page. Those new images are passed onto other models for object extraction, while others detect and decode text for indexing and applying of various graph functions.

Here's Google Vision looking at a Bloomberg article and seeing people, given Cuomo is people. That search, "cuomo people" would return this article and a picture of Cuomo.

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
*"Your ideas don't stink. Just make sure they become a reality."*

Thanks for reminding me, Igor.
