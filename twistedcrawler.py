from twisted.web.client import getPage
from twisted.internet.defer import DeferredList
# from twisted.python.util import println


def process_page(output):
	print "Page Output:{}".format(output[:100])
	return output

def process_error(output):
	print "Error: {}".format(output)

def all_processed(result):
	print "Everything has returned\nResults:{}".format(result)

def fetch_urls(reactor,url_list):
	prep_list = []
	for url in url_list:
		print "Fetching {}".format(url)
		d = getPage(url)
		d.addCallback(process_page)
		d.addErrback(process_error)
		prep_list.append(d)
	d_list = DeferredList(prep_list)
	d_list.addCallback(all_processed)
	return d_list



if __name__ == '__main__':
	urls = ['http://www.google.com','http://www.amazon.com','http://www.nytimes.com','http://www.racialicious.com','http://www.groupon.com','http://www.yelp.com']
	from twisted.internet.task import react
	react(fetch_urls,argv=(urls,))