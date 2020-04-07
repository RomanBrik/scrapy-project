# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from scrapy.linkextractors import LinkExtractor

from urllib.parse import urljoin

from ..items import QuotesLoader


class QuoteSpider(CrawlSpider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    rules = (
        Rule(LinkExtractor(allow=r'page/.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        for quote in response.xpath('//div[@class="quote"]'):
            item = QuotesLoader(selector=quote)
            item.default_output_processor = TakeFirst()

            item.add_xpath('author', '*/*[@class="author"]/text()')
            item.add_xpath('quote', 'span[@class="text"]/text()', re=r'“(.+).”')
            item.add_xpath('tags', 'div[@class="tags"]/a/text()')

            yield item.load_item()
