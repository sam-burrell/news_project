#!/usr/bin/python3
from datetime import datetime
from scrapy.conf import settings
import logging
import json
import redis

redisServer = redis.Redis(host=settings['REDIS_SERVER'], port=settings['REDIS_PORT'], charset="utf-8", decode_responses=True)

class addRedis(object):
    def process_item(self, item, spider):
        redisServer.zadd(
            'urls',
            item['url'],
            int(datetime.utcnow().strftime('%s'))
        )
        redisServer.set(item['url'],json.dumps(dict(item), ensure_ascii=False).encode('utf8'))
        #logging.info("%s" % json.dumps(dict(item), ensure_ascii=False))
        return item
