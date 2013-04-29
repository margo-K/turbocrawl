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
		if domain == self._getdomain(parent) and url not in frontier[domain][1]:
			return True
		return False

	def _process_page(self,output,url):
		destination.send((url,output))
		
	def _update_frontier(self):
		url_tuples = destination.retrieve_urls() # list of tuples:: (parent_url,links)
		for url_tuple in url_tuples:
			parent_url, links = url_tuple
			for link in links:
				if self.checkinsert(link,parent_url):

	def _fetch_urls(self):
		print "Started fetching"
		prep_list = []
		for url in self.frontier:
			if self.frontier[0] < time.time():
				print "Fetching {}".format(url)
				d = getPage(url)
				d.addCallback(self._process_page,url)
				prep_list.append(d)
		d_list = DeferredList(prep_list,consumeErrors=True)
		d_list.addCallback(self._fetch_urls)
		return d_list

