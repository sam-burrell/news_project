#!/usr/bin/python3
from scrapy.loader import ItemLoader
from scrapy.spiders import Spider
from scrapy.conf import settings
from news_crawler.items import NewsCrawlerItem
import praw


class redditSpider(Spider):
    name = 'reddit'
    reddit = praw.Reddit(client_id='I5Im00HhInCOUg',
                     client_secret='3CVzcTLjddOuxp1bw1nzqSz-puY',
                     user_agent='osx:com.samburrell.samapp:v1 (by /u/samjburrell)')

    #for submission in reddit.subreddit('learnpython').hot(limit=10):
        #parse_article(submission.title)

    def parse_article(self, response):
        item = {}
        item['headline'] = response
        return item
