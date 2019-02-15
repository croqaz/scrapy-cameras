# -*- coding: utf-8 -*-
import scrapy
from .base import BaseSpider
from .util import utc_time


class BerminghamCamerasIeSpider(BaseSpider):
    name = 'berminghamcameras.ie'
    allowed_domains = ['berminghamcameras.ie', 'www.berminghamcameras.ie']
    start_urls = [
        'https://berminghamcameras.ie/digital-slr/',
        'https://berminghamcameras.ie/compact-system-cameras/',
    ]

    def parse(self, response):
        for item in response.css('.grid-list form.cm-ajax'):
            try:
                yield self.extract_one(item)
            except Exception as err:
                self.logger.warning('Error extracting item: %s %s', self.name, err)

        next_page = response.css('.ty-pagination .ty-pagination__next::attr(href)').get()
        yield self.follow_next_page(next_page, response)

    def extract_one(self, item):
        a = item.css('a.product-title')
        name = a.css('::text').get()
        link = a.css('::attr(href)').get()
        price = item.css('.ty-price .ty-price-num:last-child::text').get().replace(',', '')
        uid = item.css('.ty-quick-view-button>a::attr(data-ca-view-id)').get()
        return {
            'T': utc_time(),
            'link': link,
            'name': name,
            'price': float(price),
            'spider': self.name,
            'uid': uid,
        }
