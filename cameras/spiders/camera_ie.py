# -*- coding: utf-8 -*-
import scrapy
from html_text import extract_text
from .util import utc_time


class CameraIeSpider(scrapy.Spider):
    name = 'camera.ie'
    allowed_domains = ['camera.ie', 'www.camera.ie']
    start_urls = [
        'https://camera.ie/digital-cameras-dslr-mirrorless-bridge-compact-action-cam-video-camcorders/digital-cameras/dslr-cameras-professional',
        'https://camera.ie/digital-cameras-dslr-mirrorless-bridge-compact-action-cam-video-camcorders/digital-cameras/mirrorless-compact-interchangeable-lens-cameras',
    ]

    def parse(self, response):
        for item in response.css('#portfolio .product-list-item.photography'):
            try:
                yield self.extract_one(item)
            except Exception as err:
                self.logger.warning('Error extracting item: %s %s', self.name, err)

        # next_page = '???'
        # There's no pagination

    def extract_one(self, item):
        name = extract_text(item.css('.child_title').get(), guess_layout=False)
        price = item.css('.centered .styleColor::text').get()
        price = price.split('€')[-1].strip().replace(',', '')
        uid = item.xpath('//div[@class="item-box-desc"]/p/i[contains(text(), "Product Code")]/text()')
        uid = uid.get().split(':')[-1].strip()
        ean = item.xpath('//div[@class="item-box-desc"]/p/i[contains(text(), "Barcode/EAN")]/text()')
        ean = ean.get().split(':')[-1].strip()
        return {
            'T': utc_time(),
            'uid': uid,
            'ean': ean,
            'name': name,
            'price': float(price),
            'spider': self.name,
        }
