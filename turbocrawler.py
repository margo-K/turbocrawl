import urllib2
import unittest

class Crawler:
	"""Crawler will take a given page as input, 
	grab its contents and spit them out to some outside process"""

	def __init__(self):
		pass

	def grab(self,url):
		print url
		try:
			open_url = urllib2.urlopen(url)
		except urllib2.HTTPError as e:
			print "Could not open {url}: {} {}".format(e.errono,e.strerror)
		return open_url.read()



class CrawlerTests(unittest.TestCase):
	def setUp(self):
		self.c = Crawler()
		self.urls = ['http://www.google.com','http://www.amazon.com','http://www.nytimes.com','http://www.racialicious.com','http://www.groupon.com','http://www.yelp.com']

	def test_grab(self):
		"""Tests that data returns for all urls being fed in"""
		counter = 0
		for url in self.urls:
			if self.c.grab(url):
				counter +=1
		self.assertEqual(len(self.urls),counter)

if __name__ == '__main__':
	unittest.main()



