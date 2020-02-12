# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

import os

class MyimagePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        url = request.url
        file_name = item['title'] + '/' + url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        #image_paths = [x['path'] for ok, x in results if ok]
        #if not image_paths:
        #    raise DropItem('Image Downloaded Failed')
        with open('/' + item['title'] + '/' + item['title'] + '.txt', 'ab', encoding='utf-8') as f:
            for i in item['mgnets']:
                f.write(i + '/n')
        return item


    def get_media_requests(self, item, info):
        return[Request(x, meta={'item': item}) for x in item['image_urls']]


class MyfilePipeline(object):

    def process_item(self, item, spider):
        file_path = spider.settings.get("FILE_PATH")
        columns = "title,pubtime,author,content,source\n"
        data = "" + item['title'] + "," + item['pubtime'] + "," + item['author'] + "," + item['content'] + "," + item['source'] + "\n"
        if os.path.isfile(file_path):
            with open(file_path, 'a+') as f:
                f.write(data)
        else:
            with open(file_path, 'a+') as f:
                f.write(columns)
                f.write(data)
        
        return item
    