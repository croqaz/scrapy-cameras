# -*- coding: utf-8 -*-
import scrapy
from .util import utc_time

PAGE = 1
MAX_PAGES = 5


class BerminghamCamerasIeSpider(scrapy.Spider):
    name = 'berminghamcameras.ie'
    allowed_domains = ['berminghamcameras.ie', 'www.berminghamcameras.ie']
    start_urls = [
        'https://berminghamcameras.ie/digital-slr/',
        'https://berminghamcameras.ie/compact-system-cameras/',
    ]

    def parse(self, response):
        global PAGE
        for item in response.css('.grid-list form.cm-ajax'):
            try:
                yield self.extract_one(item)
            except Exception as err:
                self.logger.warning('Error extracting item: %s %s', self.name, err)

        next_page = response.css('.ty-pagination .ty-pagination__next::attr(href)').get()
        if next_page:
            PAGE += 1
            if MAX_PAGES > 0 and PAGE > MAX_PAGES:
                return
            self.logger.info(f'--- {self.name} page {PAGE} ---')
            yield response.follow(next_page, callback=self.parse)

    def extract_one(self, item):
        name = item.css('a.product-title::text').get()
        price = item.css('.ty-price .ty-price-num:last-child::text').get().replace(',', '')
        return {
            'T': utc_time(),
            'name': name,
            'spider': self.name,
            'price': float(price),
        }
