#!/usr/bin/env python
from twisted.web.client import getPage
from twisted.internet.defer import DeferredList
from twisted.internet import reactor

from tldextract import extract
import time

class Producer(object):
	"""The producer is responsible for taking the seed urls, grabbing their data and sending it to the consumer """
	def __init__(self,seeds,destination):
		self.frontier = {}
		for url in seeds:
			domain = getdomain(url)
			frontier[domain] = [time.time(),[]] # frontier[domain] = [next crawl time, pages to be crawled]
		self.destination = destination

	def _getdomain(self,url):
		"""Returns the domain of a given url"""
		return extract(url).domain

	def _checkinsert(self,url,parent):
		"""Checks whether a url can be put into the url frontier for its domain"""
		domain = self._getdomain(url)
		if domain == self._getdomain(parent) and url not in frontier[domain][1]:
			return True
		return False

	def _process_page(self,output,url):
		destination.send((url,output))

	def start(self):
		self.fetch_urls()
		reactor.run()
	
	def stop(self):
		reactor.stop()

	def _fetch_urls(self):
		print "Started fetching"
		prep_list = []
		for url in self.frontier:
			if self.frontier[0] < time.time():
				print "Fetching {}".format(url)
				d = getPage(url)
				d.addCallback(_process_page,url)
				prep_list.append(d)
		d_list = DeferredList(prep_list,consumeErrors=True)
		d_list.addCallback(all_processed)
		return d_list

