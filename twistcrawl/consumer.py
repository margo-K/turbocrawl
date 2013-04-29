#!/usr/bin/env python

from urlparse import urljoin
from bs4 import BeautifulSoup


class Consumer(object):	
	"""The consumer is responsible for accepting html and producing content from what it's received

	Currently, it only exports urls, but it could conceivably work with an indexer
	which would do something with the other data in the page"""
	def __init__(self):
		self.raw_data = {} # key: url, value: html

	def exportlinks(self,url,data):
		"""Called to send data into the Consumer's queue"""
		self.raw_data[url] = data

	def start(self):
		"""Starts the consumer process"""
		pass
		
	def _getUrls(self,url):
		"""Returns list of unicode links"""
		data = self.raw_data[url]
		soup = BeautifulSoup(data)
		return [urljoin(url,link.get('href')) for link in soup.find_all('a')]

from twisted.web.client import getPage
from twisted.internet.defer import DeferredList
from twisted.internet import reactor


def process_page(output,url,startime):
	self.consumer.start()

def all_processed(result):
	print "Everything has returned"
	res = [item[1] for item in result if item[0]]
	return res

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

def stop(result):
	print "Stopping"
	reactor.stop()
	return result

def twist_grab(urls):
	d = fetch_urls(urls)
	d.addBoth(stop)
	reactor.run()
	return d
