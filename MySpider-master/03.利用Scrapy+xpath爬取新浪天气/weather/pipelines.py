# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WeatherPipeline(object):
    def process_item(self, item, spider):
        with open('data.txt','w',encoding='utf-8') as f:
            for index,value in enumerate(item['temperature']):
                f.write('城市:{city}\n时间:{time}\n温度:{tem}\n风向:{wind}\n'.format(city=item['city'],
                                                                                 time=item['time'][index],
                                                                                 tem=item['temperature'][index],
                                                                             wind=item['wind'][index]))
        return item
