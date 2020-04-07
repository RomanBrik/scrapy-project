# -*- coding: utf-8 -*-
import re
import datetime
import socket
import json
from urllib.parse import urljoin
from unicodedata import normalize
from w3lib.html import remove_tags

from scrapy import Spider
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, Compose, TakeFirst
from scrapy.exceptions import CloseSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from ..items import OlxAdItem, SysDataItem


class OlxPageSpider(Spider):
    name = 'olx_page'
    allowed_domains = ['olx.ua']
    start_urls = ['https://www.olx.ua/nedvizhimost/ko/']
    rules = (
        Rule(LinkExtractor(allow='\?page=\d'), follow=True),
    )

    def parse(self, response):
        if response.xpath('//span[contains(@id, "InvalidRequest")][1]'):
            raise CloseSpider('IP blocked!')
        
            # scrapping ads on a page
        ad_urls = response.xpath(
            '//td[@class="offer  "]//h3/a/@href'
        ).extract()

        for url in ad_urls:
            yield response.follow(urljoin(response.url, url), callback=self.parse_item)
        
        next_page = response.xpath('//a[@data-cy="page-link-next"]/@href').get()
        
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        

    def parse_item(self, response):
        item = ItemLoader(item=OlxAdItem(), response=response)
        item.default_output_processor = TakeFirst()

        # # address
        item.add_value('address', response.url)
        # # title
        item.add_xpath('title', '//div[@class="offer-titlebox"]/h1/text()')
        #
        # # id of advertising
        item.add_xpath(
            'number',
            '//div[@class="offer-titlebox__details"]/em/small/text()',
            re='(\d+)'
        )

        # info
        th = response.xpath(
            '//table[@class="item"]//th/text()'
        ).extract()
        td = [
            re.sub('([\t\n]+)', ', ', remove_tags(s).strip()) for s in
            response.xpath(
                '//table[@class="item"]//td[@class="value"]/strong'
            ).extract()
        ]
        item.item.setdefault('info', {th: td for th, td in zip(th, td)})

        # price if exists check https://www.olx.ua/rabota/
        price = response.xpath('//div[@class="price-label"]/strong/text()').get()
        # Обработать валюту чтобы все выводилось в гривне
        item.add_value('price', price.strip() if price is not None else 'Бесплатно')
        #
        # # phone ToDO
        phone = '+380'
        item.add_value('phone', phone)
        #
        # # description
        item.add_xpath(
            'description',
            '//div[@id="textContent"]//text()',
            Compose(
                MapCompose(str.strip),
                Join('. '),
                lambda s: normalize('NFKC', s)
            ),
            re='[^\n\r]+'
        )
        # # images links
        item.add_xpath('images', '//*[@class="photo-glow"]/img/@src')

        yield item.load_item()
        # with open('output.json', 'w') as f:
        #     json.dump(dict(item.load_item().items()), f, indent=4, ensure_ascii=False, sort_keys=True)
