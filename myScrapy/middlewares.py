# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http.response.html import HtmlResponse

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

from fake_useragent import UserAgent
import time
import random

class MyscrapySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MyscrapyDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class SeleniumDownloaderMiddleware(object):

    def __init__(self, settings):
        #chrome无窗口模式
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        #设置userAgent代理
        ua = UserAgent()
        user_agent = ua.random
        print("随机获取的UserAgent为：",user_agent)
        #chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument('--user-agent=%s' % user_agent)

        #代理IP设置
        #proxy = '58.58.213.55:8888'

        proxy = random.choice(settings.get('PROXIES'))
        print("随机获取的Proxy为： ", proxy)
        chrome_options.add_argument('--proxy-server=' + proxy)

        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['acceptSslCerts'] = True
        capabilities['acceptInsecureCerts'] = True

        self.driver = webdriver.Chrome(chrome_options = chrome_options,desired_capabilities=capabilities)

    def process_request(self,request, spider):
        self.driver.get(request.url)
        time.sleep(1)
        # try:
        #     while True:
        #         ShowMore = self.driver.find_element_by_class_name("show-more")
        #         ShowMore.click()
        #         if not ShowMore:
        #             break
        # except:
        #     pass
        source = self.driver.page_source
        self.driver.quit()
        response = HtmlResponse(url=self.driver.current_url, body=source, encoding='utf-8', request=request)
        return response
    


