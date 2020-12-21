# Grub 2.0
You may imagine Grub-2.0 as an AI powered crawler.

Grub-2.0 provides a "computed imagination function" allowing machines and humans to "see" and explore online content visually using smaller sets of personally guided data. Various machine learning models may be used to "crawl" or extract text and other images from a given page's image. The resulting data may be placed into an index where it can be searched or related to other content.

<img src="https://raw.githubusercontent.com/kordless/grub-2.0/main/docs/google_vision_example.png" width="200">

## History
[Grub "One Oh"](https://en.wikipedia.org/wiki/Grub_(search_engine)) was an Open Source search engine built to distribute the job of gathering content from the web. At one point several hundred volunteers were crawling the web for the project, sending in content deltas only when pages were noted to have changed.

Grub was sold in 2003 to Looksmart and [then again in 2007 to Wikimedia](https://readwrite.com/2007/07/27/wikia_acquires_grub_from_looksmart/), where it fell into inactivity. The original Grub team eventually found itself working at Splunk.

Grub-2.0 is the literal rebirth and expansion upon the idea of decentralized search processes using AI-powered vision systems.

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Grub.svg/440px-Grub.svg.png" width="200">

As an analagy, many people can "see" a taxi *in mind* when someone says the word *taxi* to them. Where does this imagined taxi come from when the spoken request is being processed by the mind? The ancients thought this imagery came in from internal sense organs which "saw" things "in mind" that were not real.

<img src="https://upload.wikimedia.org/wikipedia/commons/0/0c/RobertFuddBewusstsein17Jh.png" width="300">

Here is a related video discussing building machine awareness which you may find interesting:

[![synth](https://img.youtube.com/vi/frB8I5gxSXk/0.jpg)](https://www.youtube.com/watch?v=frB8I5gxSXk)

## Competition
Google provides image search functions for the massive amount of content they have crawled. Many believe that having more content in your index is better.

A few don't.

A machine or human using Grub may receive related imagery using search queries such as "robot hand" even if Grub is only shown a few pages on robot hands. This keeps things simple and secure and doesn't require scraping Google results to get imagery into your machine.

Here's an example page fragment created with Grub:

<img src="https://github.com/kordless/grub-2.0/blob/main/docs/h2ssme1AjSKfObij3DMZyQ2.jpg?raw=true" width="500">

Unlike Google, when Grub is given a site it may return one or more images and/or search indexes. Indexes can be queried later by using Solr's time or relatedness functions.

This process may be useful for testing or training machine learning models or providing new types of search features to users, such as what is being done over at [mitta.us](https://mitta.us).

## How
Grub "looks" at the page using a computed aperture implemented with Geckodriver, Firefox, Solr and various maachine learning vision models. By passing a site's image to a model, we may find and crop related images or text on the page. When image are found they may be passed onto other models for object extraction.

We can even image and extract the source code of the page (this example uses Google Vision's model):

<img src="https://raw.githubusercontent.com/kordless/grub-2.0/main/docs/index.png" width="500">

Here we see a Google Vision model looking at a Bloomberg article and seeing people, given Cuomo is people. A subsequent search, "cuomo people", would return this article and a picture of Cuomo.

<img src="https://raw.githubusercontent.com/kordless/grub-2.0/main/docs/googlevision.PNG" width="500">

Other models may be run on Tensorflow directly. We'll implement this in the very near future.

Grub runs on [Flask](https://flask.palletsprojects.com/en/1.1.x/) in Python and uses [Solr 7.5.2](https://lucene.apache.org/solr/), [Webdriver](https://github.com/SeleniumHQ/selenium) and [Tensorflow](https://github.com/tensorflow/tensorflow).

## Install
This open code repository provides information and scripts for deploying a computated aperture. This system can be used to image websites and image content.

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

Instances will be running in a few minutes, listening on port 8389 for Solr.

Yes, the default port numbers for Solr have been transposed.

### Manage Solr
Login URL looks like: http://solr:f00bark@x.x.x.x:8389

## Deploy Grub
Deploy a secure Grub instance on Google cloud:

```
$ ./deploy-grub.sh
Password token is: f00bark
```

Instances will be running in a few minutes, listening on port 8983 for Grub.


### Run Grub
A request for imaging a URL: 

```
$ curl -X POST -d "https://news.ycombinator.com/news" http://grub:f00bark@x.x.x.x:8983/g
{"result": "success", "filename": "1ORJX7BCQ6vT0J2erqu8kWd.png"}
```

On OSX, viewing the site image looks like: 
```
$ open http://grub:f00bark@34.82.44.60:8983/images/1ORJX7BCQ6vT0J2erqu8kWd.png
```

## Tensorflow
Deploy a tensorflow model. This part remains to be completed, although there is a nice Tensorflow deployment here:

[Deploy Tensorflow in 10 Minutes](https://gist.github.com/kordless/c5b445447498ff5cb28178e12a7d9b0b)

Back in Grub-2.0's directory, do the following:

```
$ ./deploy-tensorflow.sh
Password token is: f00bark
```

## Fastener
Deploy a controller box for starting instances. Not done yet, either.

```
$ ./deploy-fastener.sh
```

Instance will be running in a few minutes listening on port 80.

## Bookmark
[Bookmark and index](https://mitta.us/https://github.com/kordless/grub-2.0/) this page using [Mitta.us](https://mitta.us/).

## Credits
*"Your ideas don't stink. Just make sure they become a reality."* - **Igor Stojanovski, Author of Grub**

Thanks, Igor. I forgot this for a time, but am keeping it "clearly in mind" now.
