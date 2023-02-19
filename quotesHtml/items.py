# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


def remove_whitespace(value):
    return value.strip()


def remove_symbols(value):
    char_remove = ['"“', '“', '”"']
    for char in char_remove:
        value = value.replace(char, "")
    return value


class QuoteshtmlItem(scrapy.Item):
    author = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_whitespace),
        output_processor=TakeFirst()
    )
    quote = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_whitespace, remove_symbols),
        output_processor=TakeFirst()
    )
