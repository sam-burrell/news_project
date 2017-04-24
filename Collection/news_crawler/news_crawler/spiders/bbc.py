#!/usr/bin/python3
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Compose, Join
from scrapy.loader import ItemLoader
from scrapy.conf import settings

from news_crawler.items import NewsCrawlerItem
import ciso8601

class bbcSpider(CrawlSpider):
    name = 'bbc'
    allowed_domains = ['bbc.co.uk']
    start_urls = ['http://www.bbc.co.uk/news/']
    rules = (
        # Follow Links
        Rule(LinkExtractor(allow=settings['FOLLOW_LINK_LIST']), ),
        # Parse and follow links that match
        Rule(LinkExtractor(allow=(r'[3-9]\d{7}$', ), deny=settings['IGNORE_LINK_LIST']), callback='parse_article', follow=True),
    )

    def parse_article(self, response):
        article = ItemLoader(item=NewsCrawlerItem(), response=response)
        article.add_value('country', 'uk')
        article.add_value('language', 'english')
        article.nested_css('meta[property="og:title"]').add_xpath('headline', './@content', re=r'(.*) - BBC')
        article.add_value('url', response.url)
        # Function to parse published time to iso6801
        time_in = Compose(
            Join(),
            lambda v: '' if (ciso8601.parse_datetime(v) is None) else ciso8601.parse_datetime(v).isoformat(sep='T')
        )
        article.add_xpath(
            'published_time',
            '//*[@id="responsive-news"]/head/script[1]/text()',
            time_in,
            re=r'"datePublished": "(.*)"',
        )
        article.nested_css('meta[property="article:section"]').add_xpath('category', './@content')
        article.add_value('encoding', response.encoding)
        article.nested_css('div.story-body__inner').add_xpath('body', './p//text()')
        article.nested_css('map-body').add_xpath('body', './p//text()')
        return article.load_item()
