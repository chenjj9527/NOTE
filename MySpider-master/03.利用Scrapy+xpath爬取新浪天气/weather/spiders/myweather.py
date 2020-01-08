# -*- coding: utf-8 -*-
import scrapy
from weather.items import WeatherItem

class MyweatherSpider(scrapy.Spider):
    name = 'myweather'
    allowed_domains = ['http://weather.sina.com.cn']
    start_urls = ['http://weather.sina.com.cn/']

    def parse(self, response):
        Item=WeatherItem()
        Item['city']=response.xpath('//*[@id="slider_ct_name"]/text()').extract()
        Item['time']=response.xpath('//*[@id="blk_fc_c0_scroll"]/div/p[@class="wt_fc_c0_i_date"]/text()').extract()
        Item['temperature']=response.xpath('//*[@id="blk_fc_c0_scroll"]/div/p[@class="wt_fc_c0_i_temp"]/text()').extract()
        Item['wind']=response.xpath('//*[@id="blk_fc_c0_scroll"]/div/p[@class="wt_fc_c0_i_tip"]/text()').extract()
        return Item
        