#!/usr/bin/python3
from scrapy import signals
from scrapy.signalmanager import SignalManager
from scrapy.responsetypes import responsetypes
from scrapy.xlib.pydispatch import dispatcher
from selenium import webdriver
from six.moves import queue
from twisted.internet import defer, threads
from twisted.python.failure import Failure


class PhantomJSDownloadHandler(object):

    def __init__(self, settings):
        self.options = settings.get('PHANTOMJS_OPTIONS', {})

        max_run = settings.get('PHANTOMJS_MAXRUN', 10)
        self.sem = defer.DeferredSemaphore(max_run)
        self.queue = queue.LifoQueue(max_run)

        SignalManager(dispatcher.Any).connect(self._close, signal=signals.spider_closed)

    def download_request(self, request, spider):
        """use semaphore to guard a phantomjs pool"""
        return self.sem.run(self._wait_request, request, spider)

    def _wait_request(self, request, spider):
        try:
            driver = self.queue.get_nowait()
        except queue.Empty:
            driver = webdriver.PhantomJS(**self.options)

        driver.get(request.url)
        # ghostdriver won't response when switch window until page is loaded
        dfd = threads.deferToThread(lambda: driver.switch_to.window(driver.current_window_handle))
        dfd.addCallback(self._response, driver, spider)
