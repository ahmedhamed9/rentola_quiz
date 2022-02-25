import scrapy
from itemloaders.processors import Join
class QuizItem(scrapy.Item):
    pass
class Property(scrapy.Item):
    title = scrapy.Field(output_processor=Join())
    price = scrapy.Field(output_processor=Join())
    link = scrapy.Field(output_processor=Join())
