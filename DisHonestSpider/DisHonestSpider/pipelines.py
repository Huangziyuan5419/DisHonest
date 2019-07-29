import pymysql
from DisHonestSpider.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB


class DishonestspiderPipeline(object):
    def open_spider(self, spider):
        self.connection = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, db=MYSQL_DB,
                                          user=MYSQL_USER, password=MYSQL_PASSWORD)
        # 获取操作数据的cursor
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        # 关闭数据库连接
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        '''保存到数据库'''
        # 如果是自然人 ，根据证件号进行判断
        # 如果企业 ：根据企业名称和区域进行判断
        # 企业判断的话或者个人  需要看年龄  年龄为零为企业  否则为自然人
        if item['age'] == 0:
            # 根据企业和区域进行判断是否重复
            select_count_sql = "select count(1) from dishonest where name = '{}' and area = '{}'".\
                format(item['name'], item['area'])
        else:
            # 如果证件号是18位，那么倒数低7位倒数第四位（不包含），桑耳数字使用四个*代替
            card_num = item['card_num']
            if len(card_num) == 18:
                card_num = card_num[:-7] + "****" + card_num[-4:]
                print(card_num)
                print(len(card_num))
                item['card_num'] = card_num
            # 自热人
            select_count_sql = "select count(1) from dishonest where card_num = '{}'".format(item['card_num'])
        # 执行查询sql
        self.cursor.execute(select_count_sql)
        count = self.cursor.fetchone()[0]
        if count == 0:
            keys, values = zip(*dict(item).items())
            # 如果没数据就插入数据
            insert_sql = 'INSERT INTO dishonest ({}) VALUES ({})'.format(
                ','.join(keys),
                ','.join(['%s'] * len(values))
            )
            # 执行sql
            self.cursor.execute(insert_sql, values)
            # 提交
            self.connection.commit()
            spider.logger.info('插入数据')
        else:
            spider.logger.info('数据重复')
        return item



