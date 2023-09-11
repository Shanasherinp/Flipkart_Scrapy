# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FlipkartItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    p_name = scrapy.Field()
    p_num_ratings = scrapy.Field()
    p_price = scrapy.Field()
    p_mrp = scrapy.Field()
    p_offer = scrapy.Field()
    p_image_url = scrapy.Field()
    p_num_reviews = scrapy.Field()
    p_delivery_status = scrapy.Field()
    p_product_link = scrapy.Field()
