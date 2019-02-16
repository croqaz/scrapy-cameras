# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from .base import BaseSpider
from .util import utc_time


class JessopsSpider(BaseSpider):
    name = 'jessops.com'
    allowed_domains = ['jessops.com', 'www.jessops.com']
    start_urls = [
        'https://www.jessops.com/cameras/digital-slr-cameras',
        'https://www.jessops.com/cameras/compact-system-cameras'
    ]

    def parse(self, response):
        for item in response.css('#products-list .f-grid .details-pricing'):
            try:
                yield self.extract_one(item, response)
            except Exception as err:
                self.logger.warning('Error extracting item: %s %s', self.name, err)

        next_url = response.xpath('//ul[@class="f-pagination"]//i[text()="navigate_next"]/../@href').get()
        yield self.follow_next_page(next_url, response)

    def extract_one(self, item, response):
        link = item.css('.details>h4>a::attr(href)').get()
        info = item.css('.js-add-to-basket')
        price = info.css('::attr(data-price)').get().replace(',', '')
        return {
            'T': utc_time(),
            'link': urljoin(response.url, link),
            'name': info.css('::attr(data-name)').get(),
            'price': float(price),
            'spider': self.name,
            'uid': info.css('::attr(data-skuoffering)').get(),
        }
