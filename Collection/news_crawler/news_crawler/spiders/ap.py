#!/usr/bin/python3
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Compose, Join
from scrapy.loader import ItemLoader
from scrapy.conf import settings
import logging

from news_crawler.items import NewsCrawlerItem
import ciso8601


class apSpider(CrawlSpider):
    name = 'ap'
    allowed_domains = ['ap.org']
    start_urls = ['http://hosted.ap.org/dynamic/fronts/US?SITE=AP&SECTION=HOME']
    rules = (
        # Follow Links
        Rule(LinkExtractor(allow=settings['FOLLOW_LINK_LIST']+[r'/fronts/']), ),
        # Parse and follow links that match
        Rule(LinkExtractor(allow=(r'/stories/', ), deny=settings['IGNORE_LINK_LIST']), callback='parse_article', follow=True),
    )

    def parse_article(self, response):
        article = ItemLoader(item=NewsCrawlerItem(), response=response)
        article.add_value('country', 'usa')
        article.add_xpath('language', '//html/@lang')
        article.nested_css('span[class="headline entry-title"]').add_xpath('headline', './text()')
        article.add_value('url', response.url)
        # Function to parse published time to iso6801
        time_in = Compose(
            Join(),
            lambda v: '' if (ciso8601.parse_datetime(v) is None) else ciso8601.parse_datetime(v).isoformat(sep='T')
        )
        article.nested_css('div[class="timestamp updated"]').add_xpath(
            'published_time',
            './@title',
            time_in,
        )
        article.add_xpath('keywords', '//head/meta[@property="keywords"]/@content', lambda v: v[0].split(',') if v else None)
        article.add_value('encoding', response.encoding)
        article.nested_css('p[class="ap-story-p"]').add_xpath('body', './text()')

        return article.load_item()
