# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose

from urllib.parse import urljoin
from unicodedata import normalize

from ..items import BookLoader


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    rules = (
        Rule(LinkExtractor(allow='catalogue/page.+'), follow=True), # page links
        Rule(LinkExtractor(allow='catalogue/(?!category/books|page).*/.+'), callback='parse_book'), # items links
    )

    def parse_book(self, response):
        book = BookLoader(response=response)
        book.add_value('url', response.url)
        book.add_xpath('name', '//h1/text()')
        book.add_xpath('description', '//div[@id]/following-sibling::p/text()',
                       MapCompose(lambda string: normalize('NFKC', string.strip())),
                       re='^(.+)...more$')
        book.add_xpath('image', '//*[@id="product_gallery"]//img/@src',
                       MapCompose(lambda url: urljoin(response.url, url)))

        book_info = book.nested_xpath('//table')
        book_info.add_xpath('upc', '*[1]/td/text()')
        book_info.add_xpath('price_with_tax', '*[3]/td/text()')
        book_info.add_xpath('price_without_tax', '*[4]/td/text()')
        book_info.add_xpath('tax', '*[5]/td/text()')
        book_info.add_xpath('availability', '*[6]/td/text()', re='\d+')
        book_info.add_xpath('reviews_n', '*[7]/td/text()')

        yield book.load_item()
