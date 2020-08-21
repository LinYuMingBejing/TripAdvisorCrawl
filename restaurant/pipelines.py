# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql

class RestaurantPipeline(object):
    def __init__(self):
        dbparams={
            'host' : 'localhost',
            'port' : 3306,
            'user' : 'root',
            'password' : 'root',
            'database' : 'restaurant',
            'charset' : 'utf8mb4'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None


    def process_item(self, item, spider):
        params = (item['title'],item['res_type'],item['rating_count'],\
                item['info_url'],item['cellphone'],item['address'],item['street'],\
                item['rating'],item['comment'],item["open_time"])
        self.cursor.execute(self.sql, params)
        self.conn.commit()
        return item


    @property
    def sql(self):
        if not self._sql:
            self._sql="""
            insert into ta(id, title, res_type, rating_count, info_url, cellphone, address, street, rating, comment, open_time)
            values(null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            print(self._sql)
            return self._sql
        return self._sql