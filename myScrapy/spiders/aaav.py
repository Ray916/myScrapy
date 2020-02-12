# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from myScrapy.items import MyscrapyItem


class AaavSpider(scrapy.Spider):
    name = 'aaav'
    allowed_domains = ['http://www.nhc.gov.cn/']
    start_urls = ['http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml']
    
    news_url_xpath = "//ul[@class='zxxx_list']/li"
    next_url_xpath = "//div[@id='page_div']/div[@class='pagination_index'][2]/span[@class='arrow']"
    rules = (
        Rule(LinkExtractor(restrict_css=next_url_xpath),follow=True),
        Rule(LinkExtractor(restrict_xpaths=news_url_xpath),callback='parse_item')
    )

    def parse_item(self, response):
        
        title = response.xpath("//div[@class='list']/div[@class='tit']//text()").extract()
        pubtime = response.xpath("//div[@class='list']/div[@class='source']/span[1]//text()").extract()
        author = response.xpath("//div[@class='list']/div[@class='source']/span[@class='mr']//text()").extract()
        content = response.xpath("//div[@class='list']/div[@id='xw_box']/p[1]//text()").extract()
        source = response.xpath("//div[@class='list']/div[@id='xw_box']/p[4]//text()").extract()
        
        item = MyscrapyItem()
        item['title'] = title
        item['pubtime'] = pubtime
        item['author'] = author
        item['content'] = content
        item['source'] = source

        yield item
