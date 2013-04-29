#Turbocrawl
This project was inspired by Michael Nielsen's [How to Crawl a Quarter Billion Webpages in 40 Hours](http://www.michaelnielsen.org/ddi/how-to-crawl-a-quarter-billion-webpages-in-40-hours/) blog post.

Nielsen's crawler architecture employs threads to reduce idle time incurred when waiting
for the response from an http request. turbocrawler will instead use evented architecture 
while trying to recreate the rest of the approach described by Nielsen (url frontier, domains 
assigned to specific instances). 

Additionally, I will use basic benchmarking of individual components of the design to inform 
hypotheses about performance gains as the project scales. Any alterations to Nielsen's design
will only be made if a performance test can justify the change.

###Contents
* turbocrawler.py : crawler built for use with threads
* twistedcrawler : crawler built using Twisted

###Process
####Stage 1
* test the speed of just grabbing html using the turbocrawler grab function vs. twistedcrawler's getpage for 
  a large set of urls (try: 1000, 10000, 100000)
* predict gains incurred from using the faster option
####Stage 2
* build crawler with twisted-based architecture

###Getting Started
####Requirements
- Twisted 

###Status
* currently, each crawler only grabs html (as this is the functionality being tested in Stage One)

###Architecture



###TO-DOs:
* apply filtering to insure only clickable links get crawled (and not other things in 'href' <a> tags)
