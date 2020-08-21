# -*- coding: utf-8 -*-
import scrapy
from restaurant.items import TripadvisorItem


class TaSpider(scrapy.Spider):
    name = 'TA'
    allowed_domains = ['www.tripadvisor.com.tw']
    
    start_urls = ['https://www.tripadvisor.com.tw/Restaurants-g293913-Taipei.html']
    base_domain ='https://www.tripadvisor.com.tw'

    def parse(self, response): 
        item_urls = response.xpath('//div[@class="wQjYiB7z"]/span/a/@href').getall()
        for item_url in item_urls[1:]:
            yield scrapy.Request(self.base_domain+item_url, callback=self.parse_info)
                
        
        next_url = response.xpath('//a[@class="nav next rndBtn ui_button primary taLnk"]/@href').get()
        if next_url:
            yield scrapy.Request(url = response.urljoin(next_url), callback=self.parse)

    def parse_info(self,response):
        title = response.xpath('//h1[@class="_3a1XQ88S"]/text()').get()
        res_type = response.xpath('//a[@class="_2mn01bsa"]/text()').getall()[1:]
        res_type = ",".join(res_type)
        rating_count = response.xpath('//span[@class="_3Wub8auF"]/text()').get()
        if "," in rating_count:
            rating_count = rating_count.split(",")
            rating_count = int("".join(rating_count))
        rating_count = int(rating_count)
        open_time =  response.xpath('//span[@class="_1h0LGVD2"]/span/span[2]//text()').getall()[0]
        info_url = response.xpath('//img[@class="basicImg"]/@data-lazyurl').getall()[0:-1]
        info_url = ",".join(info_url)

        cellphone = response.xpath('//span[@class="detail  is-hidden-mobile"]/text()').get() 
        address = response.xpath('//a[@class="_15QfMZ2L"]/text()').get()
        street =  response.xpath('//a[@class="_3S6pHEQs"]/text()').get()
        rating = response.xpath('//span[@class="r2Cf69qf"]/text()').get()
        rating = float(rating)
        comment = response.xpath('//div[@class="prw_rup prw_reviews_text_summary_hsx"]/div/p[@class="partial_entry"]/text()').getall()[0:-1]
        comment = ",".join(comment)
        item = TripadvisorItem(title=title,res_type=res_type,rating_count=rating_count,info_url=info_url,cellphone=cellphone,address=address,street=street,rating=rating,comment=comment,open_time=open_time)
        yield item
