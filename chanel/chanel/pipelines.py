# pipelines.py

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import pandas as pd
import logging
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from scrapy.exceptions import DropItem
import json

class ChanelPipeline:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.items = []

    def process_item(self, item, spider):
        # 创建 item 的深拷贝，确保每个 item 是独立的对象
        item_copy = item.copy()

        # 合并 main_image_url 和 image_url 到 image_urls 列表
        all_urls = item_copy.get('all_urls', [])
        main_image_url = item_copy.get('main_image_url')
        image_url = item_copy.get('image_url')

        if isinstance(all_urls, str):
            all_urls = [all_urls]

        if main_image_url:
            if isinstance(main_image_url, str):
                all_urls.append(main_image_url)
            elif isinstance(main_image_url, list):
                all_urls.extend(main_image_url)

        if image_url:
            if isinstance(image_url, str):
                all_urls.append(image_url)
            elif isinstance(image_url, list):
                all_urls.extend(image_url)

        item_copy['all_urls'] = all_urls

        item_info = item_copy.get('item_info','')
        item_copy['item_info_json'] = json.dumps(item_info, ensure_ascii=False)


        self.items.append(item_copy)
        return item_copy

    def close_spider(self, spider):
        try:
            # 将所有 item 转换为 DataFrame
            self.logger.debug(f"Items to be saved: {self.item_copy}")
            all_data = []
            for item in self.item_copy:
                all_data.append({
                    'Item Name': item.get('item_name', ''),
                    'Main Image URL': item.get('main_image_url', ''),
                    'Price': item.get('price', ''),
                    'Page URL': item.get('page_url', ''),
                    'Recommend': item.get('recommend', ''),
                    'Description': item.get('description', ''),
                    'Image URL': item.get('image_url', ''),
                    'Product Type': item.get('product_type', ''),
                    'title type': item.get('title_type', ''),
                    'Title List': item.get('title_list', ''),
                    'product url list': item.get('product_url_list', ''),
                    'item info': item.get('item_info_json', ''),
                    'main_oss_url': item.get('main_oss_url', '')
                })

            df = pd.DataFrame(all_data)

            # 写入 Excel 文件
            df.to_excel('output.xlsx', index=False, encoding='utf-8-sig')
            self.logger.debug('数据保存成功')
        except Exception as e:
            self.logger.info('数据保存失败：{}'.format(e))

class ChanelImagesPipeline(ImagesPipeline):

    def __init__(self, store_uri, download_func=None, settings=None):
        super().__init__(store_uri, download_func)
        self.logger = logging.getLogger(__name__)

    def get_media_requests(self, item, info):
        all_urls = item.get('all_urls', [])
        if not all_urls:
            self.logger.warning(f"No image URLs found for item: {item}")
            return

        for all_url in all_urls:
            self.logger.debug(f"Requesting image URL: {all_url}")
            yield scrapy.Request(all_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['main_oss_url'] = image_paths
        self.logger.debug(f"main_oss_url: {image_paths}")
        
        return item