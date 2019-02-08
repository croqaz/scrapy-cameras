# -*- coding: utf-8 -*-
import json
import scrapy
from html_text import extract_text
from .base import BaseSpider
from .util import utc_time


class BhPhotoVideoSpider(BaseSpider):
    name = 'bhphotovideo'
    allowed_domains = ['bhphotovideo.com', 'www.bhphotovideo.com']
    start_urls = [
        'https://www.bhphotovideo.com/c/buy/SLR-Digital-Cameras/ci/6222/N/4288586280',
        'https://www.bhphotovideo.com/c/buy/Mirrorless-System-Cameras/ci/16158/N/4288586281'
    ]

    def parse(self, response):
        for item in response.css('.main-content .items .item'):
            try:
                yield self.extract_one(item)
            except Exception as err:
                self.logger.warning('Extract item error: %s %s', self.name, err)

        next_page = response.css('.pagination-zone .pn-next::attr(href)').get()
        yield self.follow_next_page(next_page, response)

    def extract_one(self, item):
        name = extract_text(item.css('.desc-zone a[itemprop="url"]').get(), guess_layout=False)
        link = item.css('.desc-zone h5 a::attr(href)').get()
        mfr = item.css('.skus .sku[data-selenium="sku"]::text').get()
        idata = json.loads(item.css('::attr(data-itemdata)').get())
        return {
            'T': utc_time(),
            'link': link,
            'mfr': mfr,
            'name': name.strip(),
            'price': float(idata['price']),
            'spider': self.name,
            'uid': idata['sku'],
        }
