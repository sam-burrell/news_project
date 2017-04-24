#!/usr/bin/python3
from scrapy.item import Item, Field
from scrapy.loader.processors import Join, MapCompose
from w3lib.html import replace_escape_chars

class NewsCrawlerItem(Item):
    uid = Field()
    language = Field(
        output_processor = Join()
    )
    country = Field(
        output_processor = Join(),
    )
    headline = Field(
        input_processor = MapCompose(lambda v: v.split(), replace_escape_chars),
        output_processor = Join()
    )
    url = Field(
        output_processor = Join()
    )
    published_time = Field(
        output_processor = Join()
    )
    modified_time = Field(
        output_processor = Join()
    )
    category = Field(
        output_processor = Join()
    )
    keywords = Field(
        output_processor = Join()
    )
    body = Field(
        input_processor = MapCompose(lambda v: v.split(), replace_escape_chars),
        output_processor = Join()
    )
    encoding = Field(
        output_processor = Join(),
    )
    stopwords = Field()
