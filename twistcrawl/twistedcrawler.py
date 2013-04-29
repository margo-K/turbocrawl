#!/usr/bin/env python
import time
import twistcrawl.consumer
import twistcrawl.producer

def Crawler(object):
	def __init__(self):
		self.consumer = Consumer()

	def start(self,seeds):
		self.produce = Producer(seeds)

	def stop(self):
		"""Eventually, stop could mean stopping the reactor or writing the current raw data (consumer) and 
		frontier (producer) to a file"""
		pass 

if __name__ == '__main__':
	urls = ['http://www.google.com','http://www.amazon.com','string','http://www.racialicious.com','http://www.groupon.com','http://www.yelp.com']
	c = Crawler()
	c.start(urls)
	time.sleep(10)
	c.stop()