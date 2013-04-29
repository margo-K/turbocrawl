TwistedCrawl
=========

TwistedCrawl is inspired by a blog post - [How to Crawl a Quarter Billion Webpages in 40 Hours](http://www.michaelnielsen.org/ddi/how-to-crawl-a-quarter-billion-webpages-in-40-hours/).

The author of the post built out a crawler architecture that works across 20 EC2 instances using a large number of threads for each one. TwistedCrawler uses a similar architecture, but instead of using threads, it uses Twisted, so all html is retrieved asynchronously. 

##How it works

The crawler asynchronously fetches html from provided links using Twisted. It starts with
a list of seed urls and performs a breadth-first traversal through the links from each page, with a few alterations:

1. each individual crawler instance only crawls links from its 'portion' of the web - i.e. its list of domains
2. a crawler actually dumps data into an indexer's 'bucket' and the indexer generates new urls


##How to use it

Each crawler instance is meant to be able to run in completely separate process. Starting with a list of seed urls, you can use the helper functions to triage them across different instances of the crawler (on separate EC2 instances, on different machines, etc.)

###One crawler instance

```python
  seeds = ['http://www.google.com','http://www.amazon.com','string','http://www.racialicious.com','http://www.groupon.com','http://www.yelp.com']

  c = Crawler()
  c.start(seeds)
  c.stop()

```

###Feeding in an indexer
If you want to do something useful with the urls:

```python

c = Crawler()
c.start(seeds)
c.index(indexer=myindexer) # Indexer Should take

```

##Status

###What works


###What doesn't work
* API as described doesn't exist
