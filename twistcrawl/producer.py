#!/usr/bin/env python
from twisted.web.client import getPage
from twisted.internet.defer import DeferredList, Deferred
from twisted.internet import reactor

from tldextract import extract
import time
import sys

def confirmation(output):
	# times = [(url,time) for (b, (url, time)) in output]
	print "All done!"
	# reactor.stop()

class Producer(object):
	"""The producer is responsible for taking the seed urls, grabbing their data and sending it to the consumer """
	def __init__(self,seeds,destination):
		self.frontier = {}
		for url in seeds:
			domain = self._getdomain(url)
			self.frontier[domain] = [time.time(),[url]] # frontier[domain] = [next crawl time, pages to be crawled]
		self.destination = destination

	def start(self):
		self._fetch_urls()
		reactor.run()
	
	def stop(self):
		reactor.stop()

	def _getdomain(self,url):
		"""Returns the domain of a given url"""
		return extract(url).domain

	def _checkinsert(self,url,parent):
		"""Checks whether a url can be put into the url frontier for its domain"""
		domain = self._getdomain(url)
		if domain == self._getdomain(parent) and url not in self.frontier[domain][1]:
			return True
		return False

	def _update_frontier(self):
		url_tuples = self.destination.retrieve_urls() # list of tuples:: (parent_url,links)
		for url_tuple in url_tuples:
			parent_url, links = url_tuple
			for link in links:
				if self._checkinsert(link,parent_url):
					entry = self.frontier[self._getdomain(link)]
					entry[1].append(link)

	def process_page(self,output,url):
		print "Processing {}".format(url)
		d = self.destination.send(url,output)
		d.addCallback(self.callback_fn)

	def callback_fn(self,data):
		print "I've called back: {}".format(data)

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
		d_list.addCallback(confirmation)
		return d_list

class FauxConsumer(object):
	def __init__(self):
		self.deferreds = {}

	def send(self,url,output):
		print "Sending {}'s data".format(url)
		self.deferreds[url] = Deferred()
		reactor.callLater(5,self.retrieve_urls,url)
		return self.deferreds[url]

	def retrieve_urls(self,url):
		"""Returns a list of tuples of the form [(parent_url,links)]"""
		self.deferreds[url].callback(url*4)	


if __name__  == '__main__':
	urls = ['http://www.google.com','http://www.amazon.com','http://www.racialicious.com','http://www.groupon.com','http://www.yelp.com']
	ttime = sys.argv[1]
	reactor.callLater(float(ttime),reactor.stop)
	p = Producer(seeds=urls,destination=FauxConsumer())
	p.start()

