# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Field
from scrapy.item import Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Compose, Identity

from w3lib.html import remove_tags
from unicodedata import normalize


class OlxAdItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    address = Field()
    title = Field(
        output_processor=Compose(MapCompose(str.strip), TakeFirst())
    )
    number = Field()
    info = Field(
        output_processor=Join('. ')
    )
    price = Field()
    phone = Field()
    description = Field()

    # Calculated fields
    images = Field(
        output_processor=MapCompose(str.split)
    )

class QuotesItem(Item):
    author = Field()
    quote = Field()
    tags = Field(
        output_processor=MapCompose(str.split)
    )


class QuotesLoader(ItemLoader):
    default_item_class = QuotesItem
    default_output_processor = TakeFirst()

class QuotesBiograohyItem(Item):
    url = Field()
    author = Field()
    born = Field()
    description = Field(
        # output_processor=Compose(MapCompose(lambda s: s[:100].strip()+'...'), TakeFirst())
    )

class QuotesBiographyLoader(ItemLoader):
    default_item_class = QuotesBiograohyItem
    default_output_processor = Compose(MapCompose(str.strip), TakeFirst())


class BookItem(Item):
    url = Field()
    name = Field()
    # author = Field()
    description = Field()
    image = Field()
    # product info
    upc = Field()
    price_with_tax = Field()
    price_without_tax = Field()
    tax = Field()
    availability = Field(
        output_processor=Compose(TakeFirst(), int)
    )
    reviews_n = Field(
        output_processor=Compose(TakeFirst(), int)
    )
    info = Field()


class BookLoader(ItemLoader):
    default_item_class = BookItem
    default_output_processor = TakeFirst()


class MovieItem(Item):
    title = Field()
    plot = Field()
    year = Field()
    rating = Field()
    runtime = Field()
    website = Field()


class MovieLoader(ItemLoader):
    default_item_class = MovieItem
    default_output_processor = TakeFirst()


class SysDataItem(Item):
    # Sys fields
    project = Field()
    spider = Field()
    server = Field()
    date = Field()


