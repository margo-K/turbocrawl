from twisted.web.client import getPage
from twisted.internet.defer import DeferredList
from twisted.internet import reactor
import time
import pdb

def process_page(output,url,startime):
	print "Processed {}".format(url)
	return url,time.time()-startime

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