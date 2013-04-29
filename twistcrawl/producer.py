#!/usr/bin/env python

from tldextract import extract

class Producer(object):
	"""The producer is responsible for taking the seed urls, grabbing their data and sending it to the consumer """
	def __init__(self,seeds):
		frontier = {}
		for url in seeds:
			domain = getdomain(url)
			frontier[domain] = [time.time(),[]] # frontier[domain] = [next crawl time, pages to be crawled]

	def _getdomain(self,url):
		"""Returns the domain of a given url"""
		return extract(url).domain

	def _checkinsert(self,url,parent):
		"""Checks whether a url can be put into the url frontier for its domain"""
		domain = self._getdomain(url)
		if domain == self._getdomain(parent) and url not in frontier[domain][1]:
			return True
		return False

	def fetch_urls(url_list):
		print "Started fetching"
		prep_list = []
		for url in url_list:
			print "Fetching {}".format(url)
			d = getPage(url)
			d.addCallback(process_page,url,time.time())
			prep_list.append(d)
		d_list = DeferredList(prep_list,consumeErrors=True)
		d_list.addCallback(all_processed)
		return d_list
