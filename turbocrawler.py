import urllib2
import unittest
import threading
from Queue import Queue

def grab(url_queue):
	# print "Started grabbing. There are {} threads alive".format(threading.active_count())
	while not url_queue.empty():
		# print "Current Queue Size: {}".format(url_queue.qsize())
		try:
			url = url_queue.get()
			open_url = urllib2.urlopen(url)
		except urllib2.HTTPError as e:
			print "Could not open {url}: {} {}".format(e.errono,e.strerror)
		else:
			print "I've opened {}".format(url)
			# print "I'm on {} and there are {} total threads".format(threading.current_thread(), threading.active_count())

			# print "There are {} active threads".format(threading.active_count())
			# url_queue.task_done()
	url_queue.task_done()


	
class Crawler:
	"""Crawler will take a given page as input, 
	grab its contents and spit them out to some outside process"""

	def __init__(self,url_list,threads=2):
		self.urls = Queue(len(url_list))
		for url in url_list:
			self.urls.put(url)
		self.num_threads = threads

	def start_crawl(self):
		for _ in xrange(self.num_threads):
			t = threading.Thread(target=grab,args=(self.urls,))
			t.daemon = True
			t.start()
			# print "Started {}".format(t.name)
		self.urls.join()

	def ship_data(self,data):
		pass




class CrawlerTests(unittest.TestCase):
	def setUp(self):
		urls = ['http://www.google.com','http://www.amazon.com','http://www.nytimes.com','http://www.racialicious.com','http://www.groupon.com','http://www.yelp.com']
		self.c = Crawler(urls,7)

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
	



	

