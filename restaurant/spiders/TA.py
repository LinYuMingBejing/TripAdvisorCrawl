# -*- coding: utf-8 -*-
import scrapy
from restaurant.items import TripadvisorItem


class TaSpider(scrapy.Spider):
    name = 'TripAdvisor'
    allowed_domains = ['www.tripadvisor.com.tw']
    
    start_urls = ['https://www.tripadvisor.com.tw/Restaurants-g293913-Taipei.html']
    base_domain ='https://www.tripadvisor.com.tw'


    def clean_address(self, address):
        strings = address.split(' ')

        if strings[0] == '台灣':
            area = strings[1]
        else:
            area = strings[2]
            
        if len(area) == 5:
            city, area = area[3:], area[:3] 
        else:
            city, area = area[2:], area[:2]
        return city, area


    def parse(self, response): 
        item_urls = response.xpath('//div[@class="wQjYiB7z"]/span/a/@href').getall()
        next_url = response.xpath('//a[@class="nav next rndBtn ui_button primary taLnk"]/@href').get()

        for item_url in item_urls[1:]:
            yield scrapy.Request(self.base_domain+item_url, callback=self.parse_info)
        
        if next_url:
            yield scrapy.Request(url = response.urljoin(next_url), callback=self.parse)


    def parse_info(self,response):
        item = TripadvisorItem()

        item['title'] = response.xpath('//h1[@class="_3a1XQ88S"]/text()').get()
        item['cellphone'] = response.xpath('//a[@class="_3S6pHEQs"]/text()').get()
        item['res_type'] = response.xpath('//a[@class="_2mn01bsa"]/text()').getall()[1:]
        item['rating'] = response.xpath('//span[@class="r2Cf69qf"]/text()').get()
        item['rating_count'] = response.xpath('//span[@class="_3Wub8auF"]/text()').get()
    
        item['open_time'] = response.xpath('//span[@class="_1h0LGVD2"]/span/span[2]//text()').getall()
        item['info_url'] = response.xpath('//img[@class="basicImg"]/@data-lazyurl').getall()
        item['comment'] = response.xpath('//div[@class="prw_rup prw_reviews_text_summary_hsx"]/div/p[@class="partial_entry"]/text()').getall()

        item['street'] = ''
        item['address'] = response.xpath('//a[@class="_15QfMZ2L"]/text()').get()
        item['city'], item['area'] = self.clean_address(item['address'])
        
        yield item
