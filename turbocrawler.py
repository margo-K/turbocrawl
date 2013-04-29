import urllib2
import unittest
import threading
from Queue import Queue

def grab(url_queue,output_queue):
	while not url_queue.empty():
		try:
			url = url_queue.get()
			open_url = urllib2.urlopen(url)
		except urllib2.HTTPError as e:
			print "Could not open {url}: {} {}".format(e.errono,e.strerror)
		else:
			print "I've opened {}".format(url)
			output_queue.put(url)
			url_queue.task_done()

class Crawler:
	"""Crawler will take a given page as input, 
	grab its contents and spit them out to some outside process"""

	def __init__(self,url_list,threads=2):
		print "Working with {} threads".format(threads)
		self.urls = Queue(len(url_list))
		for url in url_list:
			self.urls.put(url)
		self.num_threads = threads

	def start_crawl(self):
		output_queue = Queue()
		for _ in xrange(self.num_threads):
			t = threading.Thread(target=grab,args=(self.urls,output_queue))
			t.daemon = True
			t.start()
		self.urls.join()
		return output_queue

	def ship_data(self,data):
		pass
 
class CrawlerTests(unittest.TestCase):
	def setUp(self):
		urls = ['http://www.google.com','http://www.amazon.com','http://www.nytimes.com','http://www.racialicious.com','http://www.groupon.com','http://www.yelp.com']
		self.c = Crawler(urls,5)

	# def test_grab(self):
	# 	"""Tests that data returns for all urls being fed in"""
	# 	counter = 0
	# 	self.c.start_crawl()
	# 	for url in self.urls:
	# 		if self.c.grab(url):
	# 			counter +=1
	# 	self.assertEqual(len(self.urls),counter)

	def test_threads_die(self):
		self.c.start_crawl()
		self.assertEqual(1,threading.active_count())


if __name__ == '__main__':
	unittest.main()
	



	

