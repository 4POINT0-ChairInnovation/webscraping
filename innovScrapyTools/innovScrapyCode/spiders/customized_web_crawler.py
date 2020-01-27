# This code is written by Josh and Modified
# It's a Scrapy framework 
"""Custom Settings:
'LOG_LEVEL' : 'INFO' Restericting to simplest logs
'REACTOR_THREADPOOL_MAXSIZE' : 10 #The maximum limit for Twisted Reactor thread pool size. This is common multi-purpose thread pool used by various Scrapy components.
'CONCURRENT_REQUESTS' : 20 #The maximum number of concurrent (ie. simultaneous) requests that will be performed by the Scrapy downloader.
'DEPTH_LIMIT': 6 #The maximum depth that will be allowed to crawl for any site. If zero, no limit will be imposed.
'DOWNLOAD_TIMEOUT' : 180 #Maximum proccessing time for each website.
'DOWNLOAD_MAXSIZE' : 10737418 #The maximum response size (in bytes) that downloader will download.
"""
import tldextract
from pymongo import MongoClient
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import innovationScraping.utility.textExtractor as textExtractor
from innovationScraping.utility import configs as configs
from scrapy import signals
import collections


# Method to insert raw data into MongoDB
def insert_into_mongo(link, data, coll):
    ext = tldextract.extract(link)
    domain = ext.domain + "." + ext.suffix
    text = textExtractor.text_from_html(data)
    coll.update_many({"link": link},{'$set': {"website": domain, "link": link, "webContent": data, "webText": text}}, upsert=True)


def insert_httperror_into_resp_coll(response, webRespColl):
    link = response.url
    ext = tldextract.extract(link)
    domain = ext.domain + "." + ext.suffix
    status = response.status
    webRespColl.update_many({"link": link},
                            {'$set': {"website": domain, "link": link, "status": status, "errMsg": response.body,
                                     }},
                            upsert=True)


def insert_into_resp_coll(failure, webRespColl):
    errMsg = failure.getErrorMessage()
    errType = str(failure.type)
    link = failure.request.url
    ext = tldextract.extract(link)
    domain = ext.domain + "." + ext.suffix
    webRespColl.update_many({"link": link},
                            {'$set': {"website": domain, "link": link, "errType": errType, "errMsg": errMsg}},
                            upsert=True)

# Spider class, crawling is initiated here
class InnovSpider(CrawlSpider):
    # Custom Settings to override the default setting by Scrapy
    name = "innovScrapyCode"  # Name of Spider
    # Rules of Crawler. To deny more url formats such as blogs, forums, etc. add them to deny=
    rules = (
                Rule(LinkExtractor(deny=()), callback="parse_item", follow=True, process_request='process_request'),
            )
    requestLimit = 1000
    requestCount = collections.defaultdict(int)

    def parse_item(self, response):  # Scrapy parsed item results
        link = response.url
        ext = tldextract.extract(link)
        domain = ext.domain + "." + ext.suffix
        if (domain in self.allowed_domains):  # Only handle the results inside allowed domain.
            if (response.status == 200):
                insert_into_mongo(response.url, response.text, self.coll)

    def parse_error(self, failure):
        insert_into_resp_coll(failure, self.webRespColl)

    def process_request(self, request):
        ext = tldextract.extract(request.url)
        domain = ext.domain + "." + ext.suffix
        if self.requestCount[domain] < self.requestLimit:
            self.requestCount[domain] += 1
            return request
        else:
            #print('page Number Limit reached for ' + domain)
            return None

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(InnovSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):  # close te mongodb session after each parse
        self.client.close()

    def __init__(self,*a, **kw):
        super(InnovSpider, self).__init__(*a, **kw)
        fileIndex = kw.get('fileIndex')
        print('fileIndex:' + str(fileIndex))
        sites_file = configs.getSiteFile(fileIndex)
        with open(sites_file) as sites:
            urls = []
            allowedDomains = []
            for url in sites:
                url = url.strip("\n")
                url = url.strip()
                url = "http://www."+url
                ext = tldextract.extract(url)
                domain = ext.domain + "." + ext.suffix
                allowedDomains.append(domain)
                urls.append(url)
        print(urls)
        self.allowed_domains = allowedDomains
        self.start_urls = urls
        self.handle_httpstatus_list = [403, 404, 406, 430, 500, 502, 503]
        self.client = MongoClient()  # connects to the default host and port
        self.coll = configs.getScrapedDataColl(self.client)
        self.webRespColl = configs.getWebRespColl(self.client)