# Define here the models for your scraped s
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/s.html

import scrapy

class ChanelItem(scrapy.Item):
    #商品详情主图
    main_image_url = scrapy.Field()
    #商品图片下载地址
    main_oss_url = scrapy.Field()
    #详情商品名称
    item_name = scrapy.Field()
    #商品详情信息
    item_info = scrapy.Field()
    #商品价格
    price = scrapy.Field()
    #商品详细建议
    recommend = scrapy.Field()
    #商品描述
    description = scrapy.Field()
    #详情页其他图片url
    image_url = scrapy.Field()
    #详情页url
    page_url = scrapy.Field()
    #分类title
    title_type = scrapy.Field()
    #商品列表分类
    product_type_url = scrapy.Field()
    #商品列表url
    product_url_list = scrapy.Field()
    #商品title列表
    title_list = scrapy.Field()
    #目录url
    catelogue_url = scrapy.Field()
    #目录title
    catelogue_title = scrapy.Field()
    #需要下载的图片链接
    all_urls = scrapy.Field()
    #商品信息json文件
    item_info_json = scrapy.Field()