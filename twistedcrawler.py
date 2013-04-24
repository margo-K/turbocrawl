from twisted.web.client import getPage
from twisted.internet.defer import DeferredList
import time


def process_page(output,url):
	print "Processed {}".format(url)
	return url,time.time()

def all_processed(result):
	print "Everything has returned\nResults:{}".format(result)

def fetch_urls(reactor,url_list):
	prep_list = []
	for url in url_list:
		print "Fetching {}".format(url)
		d = getPage(url)
		d.addCallback(process_page,url)
		prep_list.append(d)
	d_list = DeferredList(prep_list,consumeErrors=True)
	d_list.addCallback(all_processed)
	return d_list

def twist_grab(urls):
	from twisted.internet.task import react
	react(fetch_urls,argv=(urls,))




if __name__ == '__main__':
	urls = ['http://www.google.com','http://www.amazon.com','string','http://www.racialicious.com','http://www.groupon.com','http://www.yelp.com']
	twist_grab(urls)