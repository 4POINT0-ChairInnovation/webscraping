# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from urllib.parse import urlparse

from innovationScraping.utility import configs as configs


class ExceptionMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    # @classmethod
    # def from_crawler(cls, crawler):
    #     # This method is used by Scrapy to create your spiders.
    #     s = cls()
    #     crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
    #     return s

    # def process_spider_input(response, spider):
    #     # Called for each response that goes through the spider
    #     # middleware and into the spider.
    #
    #     # Should return None or raise an exception.
    #     return None

    # def process_spider_output(response, result, spider):
    #     # Called with the results returned from the Spider, after
    #     # it has processed the response.
    #
    #     # Must return an iterable of Request, dict or Item objects.
    #     for i in result:
    #         yield i

    def insert_into_resp_coll(self, response, exception, webRespColl):
        errMsg = exception.getErrorMessage()
        errType = str(exception.type)
        link = response.url
        domain = urlparse(link).hostname
        domain = domain.replace('www.', '')
        webRespColl.update_many({"link": link},
                                {'$set': {"website": domain, "link": link, "errType": errType, "errMsg": errMsg}},
                                upsert=True)


    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.
        webRespColl = configs.getWebRespColl()
        #insert_into_resp_coll(response, exception, webRespColl)
        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return None

    # def process_start_requests(start_requests, spider):
    #     # Called with the start requests of the spider, and works
    #     # similarly to the process_spider_output() method, except
    #     # that it doesn’t have a response associated.
    #
    #     # Must return only requests (not items).
    #     for r in start_requests:
    #         yield r

    # def spider_opened(self, spider):
    #     spider.logger.info('Spider opened: %s' % spider.name)
