from twisted.web.client import getPage
from twisted.internet.defer import DeferredList
from twisted.internet import reactor
from tldextract import extract
import time
import pdb
import Queue
from bs4 import BeautifulSoup
from soupselect import select
from urlparse import urljoin


class Producer(object):
	def __init__(self,seeds):
		frontier = {}
		for url in seeds:
			domain = getdomain(url)
			frontier[domain] = [time.time(),[]] # frontier[domain] = [next crawl time, pages to be crawled]


	def getdomain(self,url):
		"""Returns the domain of a given url"""
		return extract(url).domain

	def checkinsert(self,url,parent):
		"""Checks whether a url can be put into the url frontier for its domain"""
		domain = self.getdomain(url)
		if domain == self.getdomain(parent) and url not in frontier[domain][1]:
			return True
		return False

class Consumer(object):	
	def __init__(self):
		self.raw_data = {} # key: url, value: html

	def send(url,data):
		"""Called to send data into the Consumer's queue"""
		self.raw_data[url] = data

	def getUrls(self,url):
		"""Returns list of unicode links"""
		data = self.raw_data[url]
		soup = BeautifulSoup(data)
		return [urljoin(url,link.get('href')) for link in soup.find_all('a')]



def process_page(output,url,startime):
	

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
	# pdb.set_trace()
	reactor.run()
	return d




if __name__ == '__main__':
	urls = ['http://www.google.com','http://www.amazon.com','string','http://www.racialicious.com','http://www.groupon.com','http://www.yelp.com']
	twist_grab(urls)
	print "Finished!"