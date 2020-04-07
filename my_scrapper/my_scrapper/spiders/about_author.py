# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapy.loader.processors import TakeFirst, MapCompose, Compose

from urllib.parse import urljoin
import requests

from ..items import QuotesBiographyLoader


class AboutAuthorSpider(CrawlSpider):
    name = 'about_author'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    # authors_urls = set()
    rules = (
        Rule(LinkExtractor(allow='page/.*'), follow=True),
        Rule(LinkExtractor(allow='author/.+', unique=True), callback='parse_author'),
    )

    def parse_author(self, response):

        item = QuotesBiographyLoader(response=response)

        item.add_value('url', response.url)
        item.add_xpath('author', '//h3/text()')
        item.add_xpath('born', '//*[@class="author-born-date"]/text()')
        item.add_xpath('description', '//*[@class="author-description"]/text()')

        yield item.load_item()
