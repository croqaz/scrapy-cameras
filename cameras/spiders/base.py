import scrapy
from .util import is_valid_url


class BaseSpider(scrapy.Spider):

    MAX_PAGES = 3

    def start_requests(self):
        if hasattr(self, 'pages'):
            max_pages = getattr(self, 'pages')
            try:
                self.max_pages = int(max_pages)
                if self.max_pages < 0:
                    self.max_pages = 0
            except Exception as err:
                self.logger.warning('Parse pages error: %s %s', max_pages, err)
                self.max_pages = self.MAX_PAGES
        else:
            self.max_pages = self.MAX_PAGES

        for next_url in self.start_urls:
            yield scrapy.Request(next_url, self.parse)

    def follow_next_page(self, url, response):
        if url and is_valid_url(url):
            self.logger.info('Next page to follow: %s', url)
            page = response.meta.get('page', 1)
            if self.max_pages > 0 and page > self.max_pages:
                self.logger.info('--- max number of pages: %i ---', self.max_pages)
                return

            self.logger.info(f'--- {self.name} page {page}/{self.max_pages} ---')
            page += 1
            meta = response.meta
            meta.update({'page': page})
            return response.follow(url, meta=meta, callback=self.parse)
