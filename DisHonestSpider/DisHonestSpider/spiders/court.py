# -*- coding: utf-8 -*-
import scrapy
import json
from jsonpath import jsonpath
from datetime import datetime
from DisHonestSpider.items import DishonestItem


class GourtSpider(scrapy.Spider):
    name = 'court'
    allowed_domains = ['court.gov.cn']
    # start_urls = ['http://court.gov.cn/']
    post_url = 'http://jszx.court.gov.cn/api/front/getPublishInfoPageList'

    def start_requests(self):
        data = {
            'pageSize': '10',
            'pageNo': '1',
        }
        # 构建post请求  交给引擎
        yield scrapy.FormRequest(self.post_url, formdata=data, callback=self.parse)

    def parse(self, response):
        # 解析页面
        results = json.loads(response.text)
        # 解析第一页的数据  获取总页数
        page_count = jsonpath(results, "$..pageCount")[0]
        # print(page_count)
        for page in range(page_count):
            formdata = {
                'pageSize': '10',
                'pageNo': str(page),
            }
            yield scrapy.FormRequest(self.post_url, formdata=formdata, callback=self.parse_data)

    def parse_data(self, response):
        '''解析数据'''
        results = json.loads(response.text)
        # 获取失信人的信息列表
        datas = results['data']
        for data in datas:
            for result in results:
                item = DishonestItem()
                # 姓名
                item['name'] = data['name']
                # 证件号
                item['card_num'] = data['cardNum']
                # 失信人年龄  企业年龄都是零
                item['age'] = int(data['age'])
                # 区域
                item['area'] = data['areaName']
                # 法人
                item['business_entity'] = data['buesinessEntity']
                # 失信内容
                item['content'] = data['duty']
                # 公布日期
                item['publish_date'] = data['publishDate']
                # 公布执行单位
                item['publish_unit'] = data['courtName']
                # 创建日期
                item['create_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # 更新日期
                item['update_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # print(item)
                yield item