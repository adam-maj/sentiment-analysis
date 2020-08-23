import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags

def remove_whitespace(value):
    return value.strip()

def remove_filler_rating(value):
    return int(value.strip('<span class="ui_bubble_rating bubble_0"></span>'))

class ReviewItem(scrapy.Item):
    review = scrapy.Field(
        input_processor = MapCompose(remove_tags, remove_whitespace),
        output_processor = TakeFirst()
    )

    rating = scrapy.Field(
        input_processor = MapCompose(remove_filler_rating),
        output_processor = TakeFirst()
    )
