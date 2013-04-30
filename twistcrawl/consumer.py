#!/usr/bin/env python

from urlparse import urljoin
from bs4 import BeautifulSoup

class Consumer(object):	
	"""The consumer is responsible for accepting html and producing content from what it's received

	Currently, it only exports urls, but it could conceivably work with an indexer
	which would do something with the other data in the page"""
	def __init__(self):
		self.raw_data = {} # key: url, value: html

	def send(self,tup):
		url = tup[0]
		data = tup[1]
		self.raw_data[url] = data
	
	def retrieve_urls(self):
		output = []
		for item in self.raw_data.iteritems:
			output.append((url,self._getUrls(url)))
		return output

		
	def _getUrls(self,url):
		"""Returns list of unicode links"""
		data = self.raw_data[url]
		soup = BeautifulSoup(data)
		return [urljoin(url,link.get('href')) for link in soup.find_all('a')]

