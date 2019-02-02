# -*- coding: utf-8 -*-
import scrapy

PAGE = 1
MAX_PAGES = 5


class JessopsSpider(scrapy.Spider):
    name = 'jessops'
    allowed_domains = ['jessops.com', 'www.jessops.com']
    start_urls = [
        'https://www.jessops.com/cameras/digital-slr-cameras',
        'https://www.jessops.com/cameras/compact-system-cameras?fh_view_size=21&fh_refview=lister&fh_reffacet=categories&fh_refpath=facet_1'
    ]

    def parse(self, response):
        global PAGE
        for item in response.css('#products-list .f-grid .details-pricing'):
            try:
                yield self.extract_one(item)
            except Exception as err:
                self.logger.warning('Error extracting item: %s %s', self.name, err)

        next_page = response.xpath('//ul[@class="f-pagination"]//i[text()="navigate_next"]/../@href').get()
        if next_page:
            PAGE += 1
            if PAGE >= MAX_PAGES:
                return
            self.logger.info(f'--- {self.name} page {PAGE} ---')
            yield response.follow(next_page, callback=self.parse)

    def extract_one(self, item):
        info = item.css('.js-add-to-basket')
        price = info.css('::attr(data-price)').get().replace(',', '')
        return {
            'spider': self.name,
            'name': info.css('::attr(data-name)').get(),
            'sku': info.css('::attr(data-skuoffering)').get(),
            'price': float(price),
        }
