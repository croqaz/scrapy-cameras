# -*- coding: utf-8 -*-
import scrapy
from .util import utc_time

PAGE = 1
MAX_PAGES = 3


class PhotospecialistIeSpider(scrapy.Spider):
    name = 'photospecialist.ie'
    allowed_domains = ['photospecialist.ie', 'www.photospecialist.ie']
    start_urls = [
        'https://www.photospecialist.ie/dslr-camera/',
        'https://www.photospecialist.ie/mirrorless-camera/',
        'https://www.photospecialist.ie/full-frame-camera/',
    ]

    def parse(self, response):
        global PAGE
        for item in response.css('ul.products-grid li.item'):
            try:
                yield self.extract_one(item, response)
            except Exception as err:
                self.logger.warning('Error extracting item: %s %s', self.name, err)

        next_page = response.css('.pages a.next::attr(href)').get()
        if next_page:
            PAGE += 1
            if MAX_PAGES > 0 and PAGE > MAX_PAGES:
                return
            self.logger.info(f'--- {self.name} page {PAGE} ---')
            yield response.follow(next_page, callback=self.parse)

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
