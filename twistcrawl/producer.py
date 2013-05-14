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
import pprint
import pdb

def confirmation(output,round_count,fn):
	print "All done with crawl round {}!".format(round_count)
	fn()

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
			self.frontier[domain] = [0,[url],0] # frontier[domain] = [next crawl time, pages to be crawled]
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

	def _update_frontier(self,parent_url,links):
		domain = self._getdomain(parent_url)
		last_location = len(self.frontier[domain][1])
		self.frontier[domain][2] = last_location
		for link in links:
			if domain == self._getdomain(link) and link not in self.frontier[domain][1]:
				self.frontier[domain][1].append(link)
				self.frontier[domain][0]=time.time()+70 # Next acceptable crawl time is 70 seconds from now

	def callback_fn(self,data):
		url = data[1]
		links = data[0]
		print "I've called back. I will be adding links to the frontier because of {}".format(data[1])
		self._update_frontier(url,links)

	def process_page(self,output,url):
		print "Processing {}".format(url)
		d = self.destination.send(url,output)
		d.addCallback(self.callback_fn) # function that gets called back when the stuff from sending returns (i.e. the list of urls)

	def _fetch_urls(self):
		print "Started fetching"
		pdb.set_trace()
		prep_list = []
		for domain in self.frontier:
			frontier = self.frontier[domain]
			if time.time()>frontier[0]:
				print "{} is okay to recrawl.".format(domain)
				try:
					for url in frontier[1][frontier[2]:]:
						print "Fetching {}".format(url)
						d = getPage(url)
						d.addCallback(self.process_page,url)
						prep_list.append(d)
				except IndexError:
					print "Nothing left to crawl"
		d_list = DeferredList(prep_list,consumeErrors=True)
		pdb.set_trace()
		self.crawlcount+=1
		d_list.addCallback(confirmation,self.crawlcount,self._fetch_urls)
		print "These are the callbacks for the list: {}".format(d_list.callbacks)
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
		self.retrieve_urls(url)
		return self.deferreds[url]
	
	def retrieve_urls(self,url):
		print "Retrieving urls from {}".format(url)
		links = get_page_links(prep_page(self.raw_data[url]))
		formatted_urls = format_urls(parent_url=url,url_list=links)
		self.deferreds[url].callback((formatted_urls,url))

if __name__  == '__main__':
	urls = ['http://www.google.com','http://www.amazon.com','http://www.racialicious.com','http://www.groupon.com','http://www.yelp.com']
	if len(sys.argv)==2:
		ttime = sys.argv[1]
		reactor.callLater(float(ttime),reactor.stop)
		p = Producer(seeds=urls,destination=Consumer())
		p.start()
	else:
		print "Please retry with a time parameter."

