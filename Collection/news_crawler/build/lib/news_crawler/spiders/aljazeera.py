#!/usr/bin/python3
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Compose, Join
from scrapy.loader import ItemLoader
from scrapy.conf import settings

from news_crawler.items import NewsCrawlerItem
from datetime import datetime

class aljazeeraSpider(CrawlSpider):
    name = 'aljazeera'
    allowed_domains = ['www.aljazeera.com']
    start_urls = ['http://www.aljazeera.com']
    rules = (
        # Follow Links
        Rule(LinkExtractor(allow=settings['FOLLOW_LINK_LIST']), ),
        # Parse Links that match
        Rule(LinkExtractor(allow=(r'\d{9}', ), deny=settings['IGNORE_LINK_LIST']), callback='parse_article', follow=True),
    )

    def parse_article(self, response):
        article = ItemLoader(item=NewsCrawlerItem(), response=response)
        article.add_value('country', 'middle east')
        article.add_value('language', 'english')
        article.add_value('stopwords', ['al', 'jazeera'])
        article.nested_css('div.article-body').add_xpath('body', './p//text()')
        article.nested_css('meta[property="og:title"]').add_xpath('headline', './@content')
        # Function to parse published time to iso6801
        published_time_in = Compose(
            Join(),
            lambda v: '' if (datetime.strptime(v, '%a, %d %B %Y %H:%M:%S %Z') is None) else datetime.strptime(v, '%a, %d %B %Y %H:%M:%S %Z').isoformat(sep='T')
        )
        article.nested_css('meta[name="LastModifiedDate"]').add_xpath(
            'published_time',
            './@content',
            published_time_in,
        )
        article.nested_css('span.article-topics').add_xpath('category', './/text()')
        article.nested_css('meta[property="ContentType"]').add_xpath('category', './@content')
        article.add_value('url', response.url)
        article.add_value('encoding', response.encoding)
        return article.load_item()
