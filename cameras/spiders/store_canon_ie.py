# -*- coding: utf-8 -*-
import json
import scrapy
from urllib.parse import urljoin
from .util import utc_time

PAGE = 1
MAX_PAGES = 3


class StoreCanonIeSpider(scrapy.Spider):
    name = 'store.canon.ie'
    allowed_domains = ['store.canon.ie']
    start_urls = [
        'https://store.canon.ie/entry-level-dslr-cameras/',
        'https://store.canon.ie/advanced-dslr-cameras/',
        'https://store.canon.ie/professional-dslr-cameras/',
        'https://store.canon.ie/mirrorless-cameras/',
    ]

    def parse(self, response):
        global PAGE
        for item in response.css('.layout .layout-items-container .layout-item'):
            try:
                yield self.extract_one(item, response)
            except Exception as err:
                self.logger.warning('Error extracting item: %s %s', self.name, err)

        next_page = response.css('ul.pagination--list li.pagination-next a::attr(href)').get()
        if next_page:
            PAGE += 1
            if MAX_PAGES > 0 and PAGE > MAX_PAGES:
                return
            self.logger.info(f'--- {self.name} page {PAGE} ---')
            yield response.follow(next_page, callback=self.parse)

    def extract_one(self, item, response):
        a = item.css('.product-tile--header>a')
        link = a.css('::attr(href)').get()
        idata = json.loads(a.css('::attr(data-analytics)').get())
        uid = idata['product'][0]['productInfo']['productID']
        name = idata['product'][0]['productInfo']['productName']
        price = idata['product'][0]['price']['priceWithTax']
        return {
            'T': utc_time(),
            'uid': uid,
            'name': name,
            'link': urljoin(response.url, link),
            'price': float(price),
            'spider': self.name,
        }
