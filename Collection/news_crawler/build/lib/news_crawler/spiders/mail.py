#!/usr/bin/python3
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Compose, Join
from scrapy.loader import ItemLoader
from scrapy.conf import settings
import logging

from news_crawler.items import NewsCrawlerItem
import ciso8601


class mailSpider(CrawlSpider):
    name = 'mail'
    allowed_domains = ['www.dailymail.co.uk']
    start_urls = ['http://www.dailymail.co.uk']
    rules = (
        # Follow Links
        Rule(LinkExtractor(allow=settings['FOLLOW_LINK_LIST']), ),
        # Parse and follow links that match
        Rule(LinkExtractor(allow=(r'article\-\d*', ), deny=settings['IGNORE_LINK_LIST']), callback='parse_article', follow=True),
    )

    def parse_article(self, response):
        article = ItemLoader(item=NewsCrawlerItem(), response=response)
        article.add_value('country', 'uk')
        article.add_xpath('language', '//html/@lang')
        article.add_xpath('headline', '//head/meta[@property="og:title"]/@content')
        article.add_value('url', response.url)
        # Function to parse published time to iso6801
        time_in = Compose(
            Join(),
            lambda v: '' if (ciso8601.parse_datetime(v) is None) else ciso8601.parse_datetime(v).isoformat(sep='T')
        )
        article.nested_css('meta[property="article:published_time"]').add_xpath(
            'published_time',
            './@content',
            time_in,
        )
        article.add_xpath('category', '//head/meta[@property="keywords"]/@content', lambda v: v[0].split(',') if v else None)
        article.add_value('encoding', response.encoding)
        article.nested_css('div[itemprop="articleBody"]').add_xpath('body', './p//text()')

        return article.load_item()
