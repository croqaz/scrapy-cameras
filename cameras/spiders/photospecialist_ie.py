# -*- coding: utf-8 -*-
import scrapy
from .base import BaseSpider
from .util import utc_time


class PhotoSpecialistIeSpider(BaseSpider):
    name = 'photospecialist.ie'
    allowed_domains = ['photospecialist.ie', 'www.photospecialist.ie']
    start_urls = [
        'https://www.photospecialist.ie/dslr-camera/',
        'https://www.photospecialist.ie/mirrorless-camera/',
        'https://www.photospecialist.ie/full-frame-camera/',
    ]

    def parse(self, response):
        for item in response.css('ul.products-grid li.item'):
            try:
                yield self.extract_one(item, response)
            except Exception as err:
                self.logger.warning('Extract item error: %s %s', self.name, err)

        next_url = response.css('.pages a.next::attr(href)').get()
        yield self.follow_next_page(next_url, response)

    def extract_one(self, item, response):
        a = item.css('.h2.product-name a')
        name = a.css('::text').get().strip()
        link = a.css('::attr(href)').get()
        # Make sure to select the correct price
        price = item.css('.price-info .price-box .price::text').getall()
        price = price[-1].strip().replace('€', '').replace(',', '')
        uid = item.css('.compare-checkbox-label-container input[type="checkbox"]::attr(value)').get()
        return {
            'T': utc_time(),
            'uid': uid,
            'name': name,
            'link': link,
            'price': float(price),
            'spider': self.name,
        }
