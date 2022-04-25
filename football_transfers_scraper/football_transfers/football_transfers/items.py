import scrapy


class FootballTransfersItem(scrapy.Item):
    data_dict = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
