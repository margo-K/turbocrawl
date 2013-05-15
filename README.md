TwistedCrawl
=========

TwistedCrawl is inspired by a blog post - [How to Crawl a Quarter Billion Webpages in 40 Hours](http://www.michaelnielsen.org/ddi/how-to-crawl-a-quarter-billion-webpages-in-40-hours/).

The author of the post built out a crawler architecture that works across 20 EC2 instances using a large number of threads to reduce idle time incurred when waiting for an http request response. TwistedCrawler instead uses Twisted to produce an evented architecture so all html is retrieved asynchronously. 

##How it works

The crawler asynchronously fetches html from provided links using Twisted. It starts with
a list of seed urls and performs a breadth-first traversal through the links from each page, with a few alterations:

1. each individual crawler instance only crawls links from its 'portion' of the web - i.e. its list of domains
2. a crawler actually dumps data into an indexer's 'bucket' and the indexer generates new urls


##How to use it

Each crawler instance is meant to be able to run in completely separate process. Starting with a list of seed urls, you can use helper functions to triage them across different instances of the crawler (on separate EC2 instances, on different machines, etc.)

##Examples
###One crawler, running for 100 seconds on a list of 6 seed urls

```bash
$python producer.py 100

Started fetching
Fetching http://www.racialicious.com
Fetching http://www.amazon.com
Fetching http://www.google.com
Fetching http://www.groupon.com
Fetching http://www.yelp.com
Processing http://www.google.com
Sending http://www.google.com's data
Processing http://www.groupon.com
Sending http://www.groupon.com's data
Processing http://www.racialicious.com
Sending http://www.racialicious.com's data
Processing http://www.amazon.com
Sending http://www.amazon.com's data
Processing http://www.yelp.com
Sending http://www.yelp.com's data
All done!


```


##Status
###What works
* the deferreds are returning when they should


###What doesn't work
* the callback function they are provided are not the correct ones
