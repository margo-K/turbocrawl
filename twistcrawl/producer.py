#!/usr/bin/env python
from twisted.web.client import getPage
from twisted.internet.defer import DeferredList, Deferred
from twisted.internet import reactor
from urlparse import urljoin
import pprint 

from tldextract import extract
import time
import sys
from bs4 import BeautifulSoup

def confirmation(output,round_count):
	print "All done with crawl round {}!".format(round_count)

def normalize(url):
    return url if url.endswith('/') else url + '/'

def prep_page(html):
	return BeautifulSoup(html)

def get_page_links(bs4_soup):
	"""Returns a list of href links in a page"""
	return [link.get('href') for link in bs4_soup.find_all('a')]
	
def format_urls(parent_url,url_list):
	"""Returns a set of absolute urls
	* anchor tags are removed
	* all urls are normalized to end with a '/' """
	return set([normalize(urljoin(parent_url,url).split('#')[0]) for url in url_list])

class Producer(object):
	"""The producer is responsible for taking the seed urls, grabbing their data and sending it to the consumer """
	def __init__(self,seeds,destination):
		self.frontier = {}
		for url in seeds:
			domain = self._getdomain(url)
			self.frontier[domain] = [time.time(),[url]] # frontier[domain] = [next crawl time, pages to be crawled]
		self.destination = destination
		self.crawlcount = 0

	def start(self):
		self._fetch_urls()
		reactor.run()
	
	def stop(self):
		reactor.stop()

	def _getdomain(self,url):
		"""Returns the domain of a given url"""
		return extract(url).domain

	def callback_fn(self,data,url):
		print "I've called back. I will be adding {} to the frontier because of {}".format(data,url)
		#self._update_frontier([(parent_url,links)])

	def process_page(self,output,url):
		print "Processing {}".format(url)
		d = self.destination.send(url,output)
		print "deferred from {}: {}".format(url,d)
		d.addCallback(self.callback_fn) # function that gets called back when the stuff from sending returns (i.e. the list of urls)

	def _fetch_urls(self):
		print "Started fetching"
		prep_list = []
		for domain in self.frontier:
			# if self.frontier[url][0] < time.time():
			for url in self.frontier[domain][1]:
				print "Fetching {}".format(url)
				d = getPage(url)
				d.addCallback(self.process_page,url)
				prep_list.append(d)
		d_list = DeferredList(prep_list,consumeErrors=True)
		self.crawlcount+=1
		d_list.addCallback(confirmation,self.crawlcount)
		return d_list

class FauxConsumer(object):
	def __init__(self):
		self.deferreds = {}

	def send(self,url,output):
		print "Sending {}'s data".format(url)
		self.deferreds[url] = Deferred()
		self.retrieve_urls(url)
		reactor.callLater(5,self.retrieve_urls,url)# calls this function after 5 seconds; note, without this function callbacks get executed right away (but still called)
		return self.deferreds[url]

	def retrieve_urls(self,url):
		"""Returns tuples of the form (parent_url,links)"""
		print "Retriev_urls with arg: {}".format(url)
		self.deferreds[url].callback(url*4)	#adds a callback when this funciton gets called, url*4 becomes the data from the callback

class Consumer(object):	
	"""The consumer is responsible for accepting html and producing content from what it's received

	Currently, it only exports urls, but it could conceivably work with an indexer
	which would do something with the other data in the page"""
	def __init__(self):
		self.raw_data = {} # key: url, value: html
		self.deferreds = {}

	def send(self,url,output):
		print "Sending {}'s data".format(url)
		self.raw_data[url] = output
		self.deferreds[url] = Deferred()
		reactor.callLater(3,self.retrieve_urls,url)
		return self.deferreds[url]
	
	def retrieve_urls(self,url):
		print "Retrieving urls from {}".format(url)
		links = get_page_links(prep_page(self.raw_data[url]))
		formatted_urls = format_urls(parent_url=url,url_list=links)
		self.deferreds[url].callback((formatted_urls,url))

if __name__  == '__main__':
	urls = ['http://www.google.com','http://www.amazon.com','http://www.racialicious.com','http://www.groupon.com','http://www.yelp.com']
	ttime = sys.argv[1]
	reactor.callLater(float(ttime),reactor.stop)
	p = Producer(seeds=urls,destination=Consumer())
	p.start()

