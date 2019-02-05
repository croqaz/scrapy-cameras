# -*- coding: utf-8 -*-
import json
import scrapy
from html_text import extract_text
from .util import utc_time

PAGE = 1
MAX_PAGES = 5


class BhPhotoVideoSpider(scrapy.Spider):
    name = 'bhphotovideo'
    allowed_domains = ['bhphotovideo.com', 'www.bhphotovideo.com']
    start_urls = [
        'https://www.bhphotovideo.com/c/buy/SLR-Digital-Cameras/ci/6222/N/4288586280',
        'https://www.bhphotovideo.com/c/buy/Mirrorless-System-Cameras/ci/16158/N/4288586281'
    ]

    def parse(self, response):
        global PAGE
        for item in response.css('.main-content .items .item'):
            try:
                yield self.extract_one(item)
            except Exception as err:
                self.logger.warning('Error extracting item: %s %s', self.name, err)

        next_page = response.css('.pagination-zone .pn-next::attr(href)').get()
        if next_page:
            PAGE += 1
            if MAX_PAGES > 0 and PAGE > MAX_PAGES:
                return
            self.logger.info(f'--- {self.name} page {PAGE} ---')
            yield response.follow(next_page, callback=self.parse)

    def extract_one(self, item):
        name = extract_text(item.css('.desc-zone a[itemprop="url"]').get(), guess_layout=False)
        mfr = item.css('.skus .sku[data-selenium="sku"]::text').get()
        idata = json.loads(item.css('::attr(data-itemdata)').get())
        return {
            'T': utc_time(),
            'name': name.strip(),
            'mfr': mfr,
            'sku': idata['sku'],
            'price': float(idata['price']),
            'spider': self.name,
        }
