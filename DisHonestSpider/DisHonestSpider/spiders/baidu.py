# -*- coding: utf-8 -*-
from datetime import datetime
import scrapy
import json
from jsonpath import jsonpath
from DisHonestSpider.items import DishonestItem


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['baidu.com']
    start_urls = ['https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=失信人&pn=0&rn=10&ie=utf-8&oe=utf-8']

    def parse(self, response):
        # 把响应内容的json字符串转化为字典
        results =  json.loads(response.text)
        # 取出总数据条数
        disp_num = jsonpath(results, '$..dispNum')[0]
        # print(dispNum)
        url_patten = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=失信人&pn={}&rn=10&ie=utf-8&oe=utf-8'
        for pn in range(0, disp_num, 10):
            url = url_patten.format(pn)
            yield scrapy.Request(url, callback=self.parse_data)

    def parse_data(self, response):
        data = json.loads(response.text)
        # 取出结果
        results = jsonpath(data, '$..result')[0]
        # print(len(results)
        for result in results:
            item = DishonestItem()
            # 姓名
            item['name'] = result['iname']
            # 证件号
            item['card_num'] = result['cardNum']
            # 失信人年龄  企业年龄都是零
            item['age'] = int(result['age'])
            # 区域
            item['area'] = result['areaName']
            # 法人
            item['business_entity'] = result['businessEntity']
            # 失信内容
            item['content'] = result['duty']
            # 公布日期
            item['publish_date'] = result['publishDate']
            # 公布执行单位
            item['publish_unit'] = result['courtName']
            # 创建日期
            item['create_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 更新日期
            item['update_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # print(item)
            yield item


