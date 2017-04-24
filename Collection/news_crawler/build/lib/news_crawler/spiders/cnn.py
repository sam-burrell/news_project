#!/usr/bin/python3
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Compose, Join
from scrapy.loader import ItemLoader
from scrapy.conf import settings

from news_crawler.items import NewsCrawlerItem
import ciso8601

class cnnSpider(CrawlSpider):
    name = 'cnn'
    allowed_domains = ['cnn.com']
    start_urls = ['http://www.cnn.com']
    rules = (
        # Follow Links
        Rule(LinkExtractor(allow=settings['FOLLOW_LINK_LIST']), ),
        # Parse and follow links that match
        Rule(LinkExtractor(allow=(r'\d{4}/\d\d/\d\d/', ), deny=settings['IGNORE_LINK_LIST']), callback='parse_article', follow=True),
    )

    def parse_article(self, response):
        article = ItemLoader(item=NewsCrawlerItem(), response=response)
        article.add_value('country', 'usa')
        article.add_value('language', 'english')
        article.nested_css('meta[property="og:title"]').add_xpath('headline', './@content')
        article.add_value('url', response.url)
        # Function to parse published time to iso6801
        time_in = Compose(
            Join(),
            lambda v: '' if (ciso8601.parse_datetime(v) is None) else ciso8601.parse_datetime(v).isoformat(sep='T')
        )
        article.nested_css('meta[name="pubdate"]').add_xpath(
            'published_time',
            './@content',
            time_in,
        )
        article.add_xpath('category', '//head/meta[@name="section"]/@content')
        article.add_xpath('keywords', '//head/meta[@itemprop="keywords"]/@content', re=r'(.*) -')
        article.add_value('encoding', response.encoding)
        article.nested_css('div.pg-rail-tall__body').nested_css('div.l-container').add_xpath('body', './/div[re:test(@class, "zn-.*")]/text()')
        return article.load_item()
