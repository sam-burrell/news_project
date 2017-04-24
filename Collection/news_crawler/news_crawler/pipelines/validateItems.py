#!/usr/bin/python3
from scrapy.exceptions import DropItem
import logging
import hashlib
logger = logging.getLogger(__name__)

class validateItems(object):
    def process_item(self, item, spider):
        if not 'body' in item:
            logger.info("Dropped: No Article found in: %s" % item['url'])
            raise DropItem()
        elif len(item['body']) < 100:
            logger.info("Dropped: Article to short in: %s" % item['url'])
            raise DropItem()
        if not 'headline' in item:
            logger.info("Dropped: No Headline found in: %s" % item['url'])
            raise DropItem()
        item['uid'] = hashlib.sha1(repr(item['url']).encode('utf-8')).hexdigest(),
        return item
