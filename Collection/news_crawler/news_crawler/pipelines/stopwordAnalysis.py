#!/usr/bin/python3
from scrapy.conf import settings
from more_itertools import unique_everseen
from datetime import datetime
import re
import logging

class stopwordAnalysis(object):
    def process_item(self, item, spider):
        dynamic_stop_words = [
            datetime.now().strftime('%Y'),
            datetime.now().strftime('%B'),
            datetime.now().strftime('%b'),
            spider.name,
            item['country'],
        ]
        dynamic_stop_words = dynamic_stop_words + settings['NEWS_STOPWORDS']
        if 'stopwords' in item:
            item['stopwords'] = dynamic_stop_words + item['stopwords']
        else:
            item['stopwords'] = dynamic_stop_words
        return item
