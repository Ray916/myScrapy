# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from myScrapy.items import MyscrapyItem


class AaavSpider(scrapy.Spider):
    name = 'aaav'
    allowed_domains = ['www.javbus.com']
    start_urls = ['http://www.javbus.com/']
    
    video_url_xpath = "/html/body/div[@class='container-fluid']/div[@class='row']/div[@id='waterfall']/div[@id='waterfall']/div[@class='item']/a[@class='movie-box']"
    next_url_css = "a#next"
    rules = (
        Rule(LinkExtractor(restrict_css=next_url_css),follow=True),
        Rule(LinkExtractor(restrict_xpaths=video_url_xpath),callback='parse_item')
    )

    def parse_item(self, response):
        
        title = response.xpath("/html/body/div[@class='container']/h3//text()").extract_first()
        images = response.xpath("/html/body/div[@class='container']/div[@id='sample-waterfall']/a[@class='sample-box']//img//@src").extract()
        mgnets = response.xpath("/html/body/div[@class='container']/div[@class='movie'][2]/table[@id='magnet-table']/tr/td[1]/a//@href").extract()
        
        item = MyscrapyItem()
        item['title'] = title
        item['image_urls'] = images
        item['mgnets'] = mgnets

        yield item
