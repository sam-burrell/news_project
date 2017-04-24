#!/usr/bin/python3
import logging
from scrapy import logformatter
from scrapy.exceptions import IgnoreRequest
from scrapy.conf import settings
import redis

class PoliteLogFormatter(logformatter.LogFormatter):
    def dropped(self, item, exception, response, spider):
        return {
            'level': logging.DEBUG,
            'msg': logformatter.DROPPEDMSG,
            'args': {
                'exception': exception,
                'url': response.url,
            }
        }
    def scraped(self, item, response, spider):
        if isinstance(response, logformatter.Failure):
            src = response.getErrorMessage()
            return {
                'level': logging.WARNING,
                'msg': "Error: %s" % src,
            }
        else:
            src = response
        return {
            'level': logging.INFO,
            'msg': "Scraped: %s" %item['url'],
        }


class IgnoreDuplicates():
    def process_request(self, request, spider):
        redisServer = redis.Redis(host=settings['REDIS_SERVER'], port=settings['REDIS_PORT'], charset="utf-8", decode_responses=True)
        if redisServer.exists(request.url) == 1:
            raise IgnoreRequest()
        elif redisServer.exists(request.url) == 0:
            return None


class NewsCrawlerSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
