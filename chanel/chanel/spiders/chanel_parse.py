import scrapy
from scrapy.http import HtmlResponse
from scrapy import Selector , Request
import logging
from urllib.parse import urljoin, unquote

from chanel.items import ChanelItem

class ChanelParseSpider(scrapy.Spider):
    name = "chanel_parse"
    allowed_domains = ["www.chanel.cn"]
    start_urls = ["https://www.chanel.cn/cn/fashion/handbags/c/1x1x1/",
                  "https://www.chanel.cn/cn/fashion/shoes/c/1x1x5/"]
    base_url = 'https://www.chanel.cn'
    
    custom_settings = { "scrapy.pipelines.images.ImagesPipeline": 1,  # 确保启用 Scrapy 的 ImagesPipeline
    "chanel.pipelines.ChanelPipeline": 2,
    "chanel.pipelines.ChanelImagesPipeline": 3,
    }  # 如果有自定义的图片处理管道}

    def start_requests(self):
        for url in self.start_urls:
            logging.info(f"Starting request to {url}")
            yield scrapy.Request(url=url, callback=self.parse_categorylist)
        # def parse_catelogue(self, response: HtmlResponse):
        # sel = Selector(response)
        # item = ChanelItem()
        # catelogue_Html = sel.xpath('//div[@class="header__columns"]')
        # logging.info(f"Found {len(catelogue_Html)} catelogue lists.")
        # catelogue_Htmls_lis = catelogue_Html.xpath('.//ul/li')

        # for catelogue_Html_li in catelogue_Htmls_lis:
        #     # 
        #     catelogue_url = catelogue_Html_li.xpath('.//a/@href').extract()
        #     catelogue_title = catelogue_Html_li.xpath('.//a/text()').extract()
        #     catelogue_dict = dict(zip(catelogue_url,catelogue_title))
        #     logging.info(f"k_v:{catelogue_dict}")
        #     item['catelogue_url'] = catelogue_url
        #     item['catelogue_title'] = catelogue_title
        #     for catelogue_url, catelogue_title in catelogue_dict.items():
        #         item['catelogue_title'] = catelogue_title
        #         item['catelogue_url'] = urljoin(base_url,catelogue_url)
        #         if catelogue_url and catelogue_title:

        #             yield scrapy.Request(url=unquote(catelogue_url), callback=self.parse_categorylist,meta={'item':item})
                
                

    def parse_categorylist(self, response: HtmlResponse):
        
        sel = Selector(response)

        
        chanel_List_Htmls = sel.xpath('//ul[@class="fs-container fs-container--list fs-container--paddingsDesktop-normal fs-container--paddingsResponsive-normal fs-container--center"]')
        logging.info(f"Found {len(chanel_List_Htmls)} category lists.")
        product_urls_list = chanel_List_Htmls.xpath('.//li/div/span/a/@href').extract()
        title_list = chanel_List_Htmls.xpath('.//li/div/span/a/span/text()').extract()

        categorylist_dict = dict(zip(product_urls_list,title_list))
        logging.info(f"k_v:{categorylist_dict}")
        for  product_url, title in categorylist_dict.items():
            # 提取每个产品类型列表链接
            item = ChanelItem()

            item['title_type'] = title   
            item['product_type_url'] = product_url
            if product_url and title:
                logging.info(f"get type title: {title}")
                logging.info(f"get type URL: {product_url}")
                yield scrapy.Request(url=unquote(product_url), callback=self.parse_category,meta={'item':item})

    
    def parse_category(self, response: HtmlResponse):
        sel = Selector(response)

        

        chanel_product_Html = sel.xpath('//ul[@class="fs-products-grid__product-grid fs-products-grid__product-grid_accessories"]')
        logging.info(f"Found {len(chanel_product_Html)} product lists in category.")
        product_items = chanel_product_Html.xpath('.//li')
        logging.info(f"Found {len(product_items)} products in this list.")
                # 提取产品详情链接
        for product_item in product_items:

            
            titles_2 = product_item.xpath('.//span[@class="fs-product-item__name fs-font__zh_CN--heading7"]/text()').getall()
            logging.info(f"get product titles: {titles_2}")
            product_urls_2 = product_item.xpath('.//a[@class="fs-product-item__link"]/@href').getall()
            logging.info(f"get product URLS: {product_urls_2}")
            

            category_dict = dict(zip(product_urls_2,titles_2))

            for product_url_2,title_2 in category_dict.items():
                chanel_item = response.meta['item']  
                chanel_item['product_url_list'] = product_url_2
                chanel_item['title_list'] = title_2
                logging.info(f"get product title: {title_2}")
                logging.info(f"get product URL: {product_url_2}")
                yield scrapy.Request(url=unquote(product_url_2), callback=self.parse , meta={'item':chanel_item}) 


    def parse(self, response: HtmlResponse):
        sel = Selector(response)
        chanel_item = response.meta['item']  
        chanel_items = sel.xpath('//div[@class="cc-pdp"]')


        self.logger.debug(f"Extracted title_type: {chanel_item['title_type']}")
        self.logger.debug(f"Extracted product_type: {chanel_item['product_type_url']}")
        self.logger.debug(f"Extracted title_list: {chanel_item['title_list']}")
        self.logger.debug(f"Extracted product_url_list: {chanel_item['product_url_list']}")
        for item in chanel_items:
            # 打印当前 item 的 HTML 内容
            # self.logger.debug(f"Current item HTML: {item.get()}")

            # 提取图片 URL
            # image_url = item.xpath('.//div[@class="cc-hero__content"]/picture[@class="cc-image cc-image--is-loaded cc-image--has-element-on-top cc-hero__img"]/img/@src').get()

            try:
                main_image_url = item.xpath('//div[@class="cc-hero__content"]/picture/img/@src | //div[@class="cc-hero-splitted__img-wrapper cc-hero-splitted__img-wrapper--rtw"]/picture/img/@src').get()
                self.logger.debug(f"Extracted main image URL: {main_image_url}")
            except Exception as e:
                self.logger.error(f"Error extracting image URL: {e}")

            try:
                item_name = item.xpath('//div[@class="cc-pdp"]//div/h1/span[3]//text()').get()
                self.logger.debug(f"Extracted item name: {item_name}")
            except Exception as e:
                self.logger.error(f"Error extracting image URL: {e}")    

            try:
                image_url = item.xpath('//div[@class="grid"]/ul/li/picture/img/@src').getall()
                self.logger.debug(f"Extracted image_url: {image_url}")
            except Exception as e:
                self.logger.error(f"Error extracting image URL: {e}")   
            
            try:
                price = item.xpath('//div[@class="cc-hero-content"]/p/span/text()').get()
                self.logger.debug(f"Extracted price: {price}")
            except Exception as e:
                self.logger.error(f"Error extracting price: {e}")
            
            item_info = []
            
            try:
                data = item.xpath(".//div[@class='cc-product-details__informations']/div")

                for detail_item in data:
                    # 查找每个 item 下的标签和值
                    label_element = detail_item.xpath(".//h3[@class='cc-product-details-row__title']/text()").get()
                    value_element = detail_item.xpath(".//p[@class='cc-product-details-row__value']/text()").getall()

                    # 确保找到了对应的元素后再进行处理
                    if label_element and value_element:
                        Label = label_element.strip()  # 获取并清理标签文本
                        Value = ''.join(value_element).strip()  # 获取值文本，并处理可能为空的情况

                        result_dict = {
                            'Label': Label,
                            'Value': Value
                        }
                        item_info.append(result_dict)

                self.logger.debug(f"Extracted item_info: {item_info}")
            except Exception as e:
                self.logger.error(f"Error extracting item_info: {e}")

            try:
                description = response.xpath('//div[@class="cc-hero-content"]/p[@class="cc-hero-content__description"]/strong/text()').get()
                self.logger.debug(f"Extracted description: {description}")
            except Exception as e:
                self.logger.error(f"Error extracting description: {e}")

            try:
                recommend = response.xpath('//div[@class="cc-suggestions"]/p/text()').get()
                self.logger.debug(f"Extracted recommend: {recommend}")
            except Exception as e:
                self.logger.error(f"Error extracting recommend: {e}")

            try:
                page_url = response.xpath('//head/link[3]/@href').get()
                self.logger.debug(f"Extracted page_url: {page_url}")
            except Exception as e:
                self.logger.error(f"Error extracting page_url: {e}")



            chanel_item['main_image_url'] = main_image_url
            chanel_item['item_name'] = item_name
            chanel_item['image_url'] = image_url
            chanel_item['price'] = price
            chanel_item['item_info'] = item_info
            chanel_item['recommend'] = recommend
            chanel_item['description'] = description
            chanel_item['page_url'] = page_url
            
            yield chanel_item





