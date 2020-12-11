# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql

class RestaurantPipeline(object):
    def __init__(self):
        dbparams={
            'host' : '127.0.0.1',
            'port' : 3308,
            'user' : 'root',
            'password' : 'root',
            'database' : 'restaurant',
            'charset' : 'utf8mb4'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None


    def check_type(self, item):
        item['res_type'] = ','.join(item['res_type'])
        item['info_url'] = ','.join(item['info_url'])
        item['comment'] = ','.join(item['comment'])
        item['open_time'] = ''.join(item['open_time']).replace('\xa0','')
        item['rating'] = float(item['rating'])
        item['rating_count'] = int(item['rating_count'].replace(',', ''))
        return item


    def process_item(self, item, spider):
        item = self.check_type(item)
        params = (item['title'], item['res_type'], item['rating_count'],\
                item['info_url'], item['cellphone'], item['address'], item['street'],\
                item['rating'], item['comment'], item["open_time"], item['city'], item['area'])
        self.cursor.execute(self.insert, params)
        self.conn.commit()
        return item


    @property
    def insert(self):
        if not self._sql:
            self._sql="""
                insert into ta(id, title, res_type, rating_count, info_url, cellphone, address,
                                street, rating, comment, open_time, city, area)
                values(null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            return self._sql
        return self._sql