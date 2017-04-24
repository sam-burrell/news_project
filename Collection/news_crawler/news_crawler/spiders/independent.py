#!/usr/bin/python3
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Compose, Join
from scrapy.loader import ItemLoader
from scrapy.conf import settings

from news_crawler.items import NewsCrawlerItem
import ciso8601

class independentSpider(CrawlSpider):
    name = 'independent'
    allowed_domains = ['independent.co.uk']
    start_urls = ['http://www.independent.co.uk']
    rules = (
        # Follow Links
        Rule(LinkExtractor(allow=settings['FOLLOW_LINK_LIST']), ),
        # Parse Links that match
        Rule(LinkExtractor(allow=(r'\d{6}.html$', ), deny=settings['IGNORE_LINK_LIST']), callback='parse_article', follow=True),
    )

    def parse_article(self, response):
        article = ItemLoader(item=NewsCrawlerItem(), response=response)
        article.add_value("country", 'uk')
        article.add_value("language", 'english')
        article.nested_css("div.main-content-column").add_xpath("body", './div/p//text()')
        article.add_xpath("headline", '//head/meta[@property="og:title"]/@content')
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
        article.add_xpath("category", '//head/meta[@property="article:section"]/@content')
        article.add_xpath("keywords", '//head/meta[@name="keywords"]/@content')
        article.add_value("url", response.url)
        article.add_value("encoding", response.encoding)
        return article.load_item()
