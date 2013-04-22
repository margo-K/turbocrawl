from twisted.web.client import getPage
from twisted.internet.defer import Deferred
# from twisted.python.util import println


def process_page(output):
	print "Page Output:{}".format(output[:100])

def process_error(output):
	print "Error: {}".format(output)

def fetch_urls(reactor,url_list):
	for url in url_list:
		print "Fetching {}".format(url)
		d = getPage(url)
		d.addCallback(process_page)
		d.addErrback(process_error)
	return d


if __name__ == '__main__':
	urls = ['http://www.google.com','http://www.amazon.com','http://www.nytimes.com','http://www.racialicious.com','http://www.groupon.com','http://www.yelp.com']
	from twisted.internet.task import react
	react(fetch_urls,argv=(urls,))