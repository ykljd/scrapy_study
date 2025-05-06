import scrapy
from scrapy.http import HtmlResponse
from scrapy import Selector , Request
import logging
from urllib.parse import urljoin, unquote
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from chanel.items import ChanelItem

class ChanelSpider(CrawlSpider):
    name = "allchanel_parse"
    allowed_domains = ["www.chanel.cn"]
    start_urls = ["https://www.chanel.cn"]
    custom_settings = { "scrapy.pipelines.images.ImagesPipeline": 1,  # 确保启用 Scrapy 的 ImagesPipeline
    "chanel.pipelines.ChanelPipeline": 2,
    "chanel.pipelines.ChanelImagesPipeline": 3,
    }
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="fs-RedirectBtn fs-RedirectBtn--none"]/span/a/@href')), callback='parse_category', follow=True)
    )   

    def parse_item(self, response: HtmlResponse):
        pass