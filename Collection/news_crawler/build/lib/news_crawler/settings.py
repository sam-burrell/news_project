#!/usr/bin/python3

BOT_NAME = 'news_crawler'
USER_AGENT = 'news_crawler (+http://www.asdasdasdasdas.com)'
ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 2

# Redis
REDIS_PORT = 6379
REDIS_SERVER = '192.168.56.101'

# Logging
LOG_LEVEL = 'INFO'
LOG_FORMATTER = 'news_crawler.middlewares.PoliteLogFormatter'
#LOG_FORMAT = '%(asctime)s | %(message)s'

# Scrapy modules
SPIDER_MODULES = ['news_crawler.spiders']
NEWSPIDER_MODULE = 'news_crawler.spiders'
ITEM_PIPELINES = {
    'news_crawler.pipelines.validateItems.validateItems': 100,
    'news_crawler.pipelines.stopwordAnalysis.stopwordAnalysis': 200,
    'news_crawler.pipelines.processRedis.addRedis': 400,
}
DOWNLOADER_MIDDLEWARES = {
    'news_crawler.middlewares.IgnoreDuplicates': 500,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
}

# HTTPCACHE details
HTTPCACHE_ENABLED = False
HTTPCACHE_POLICY = 'scrapy.extensions.httpcache.DummyPolicy'
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
HTTPCACHE_ALWAYS_STORE = True
HTTPCACHE_DIR = '/Users/samburrell/Documents/News Project/Collection/httpcache'

# News specific arrays
NEWS_STOPWORDS = ['news', 'regions', 'correspondent', 'reporter', 'will',
'told', 'feature', 'opinion', 'including', 'columns',
'time', 'people', 'day', 'week', 'well', 'year',
'middle', 'views', 'efforts'
]
FOLLOW_LINK_LIST = [
r'world$', r'politics$', r'news$', r'uk$', r'technology$', r'science$',
r'education$', r'buisness$',r'commentisfree$', r'culture$', r'enviroment$', r'americas$',
r'people$', r'the-big-questions$', r'uk-news$', r'middleeast\.html',
r'africa\.html', r'asia\.html', r'us-canada\.html', r'latin-america\.html',
r'europe\.html', r'politics\.html', r'us\.html', r'tech.html', r'world\.html', r'regions$', r'europe$',
r'ushome'
]
IGNORE_LINK_LIST = [
'sport', 'football', 'in-pictures', 'video', 'help', 'info' , 'pictures',
'gallery', 'picture', 'contact-us', 'co.uk/service', 'entertainment', 'food',
'drink', 'music', 'discoutcode', 'tvshowbiz'
]




# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}


# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}


# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False
