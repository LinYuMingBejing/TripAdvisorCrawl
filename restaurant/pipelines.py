# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import sqlalchemy
from sqlalchemy.orm import sessionmaker
from restaurant.models import TripAdvisor


class RestaurantPipeline(object):

    def __init__(self):
        engine = sqlalchemy.create_engine('mysql+pymysql://root:root@127.0.0.1:3308/restaurant?charset=utf8mb4')
        Session = sessionmaker(bind=engine)
        self.session = Session()


    def process_item(self, item, spider):
        res_type = ','.join(item['res_type'])
        comment = ','.join(item['comment'])
        info_url = ','.join(item['info_url'])
        rating = float(item['rating'])
        rating_count = int(item['rating_count'].replace(',', ''))
        open_time = ''.join(item['open_time']).replace('\xa0','')
        title = item['title']
        cellphone = item['cellphone']
        address = item['address']
        street = item['street']
        city = item['city']
        area = item['area']
        return item

        record = self.session.query(TripAdvisor).filter_by(title=title, address=address).first()
        if not record:
            record = TripAdvisor()

        record.title = title
        record.info_url = info_url
        record.cellphone = cellphone
        record.open_time = open_time
        record.rating = rating
        record.rating_count = rating_count
        record.comment = comment
        record.street = street
        record.address = address
        record.city = city
        record.area = area

        self.session.merge(record)
        self.session.commit()
