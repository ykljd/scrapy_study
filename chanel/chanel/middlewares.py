# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from scrapy.http import HtmlResponse
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from scrapy.utils.project import get_project_settings

import time
import logging

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class ChanelSpiderMiddleware:
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

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ChanelDownloaderMiddleware:
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
        spider.logger.info("Spider opened: %s" % spider.name)


class RandomHeaderMiddleWare:
    def __init__(self):
        self.user_agents = get_project_settings('USER_AGENTS')  

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)
        # 如果IP被限制, 可以在此下载中间件添加代理
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')       # 无界面运行
        option.add_argument('--disable-gpu')    # 禁止gpu加速
        option.add_argument("no-sandbox")       # 取消沙盒模式
        option.add_argument("disable-blink-features=AutomationControlled")  # 禁用启用Blink运行时的功能
        option.add_experimental_option('excludeSwitches', ['enable-automation'])    # 开发者模式

        service = Service(ChromeDriverManager().install())
        service.log_path = 'chromedriver.log'
        service.log_level = 'DEBUG'

        driver = webdriver.Chrome(service=service,options=option)
        # 移除 `window.navigator.webdriver`. scrapy 默认为True
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
              """
        })
        
        driver.get(request.url)
        # 设置隐式等待时间为5秒
        driver.implicitly_wait(5)

        content = driver.page_source
        driver.quit()
        return Ht