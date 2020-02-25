import scrapy

class tesco_item(scrapy.Item):
    product_url = scrapy.Field(serializer=str)
    product_id = scrapy.Field(serializer=int)
    image_url = scrapy.Field(serializer=str)
    product_title = scrapy.Field(serializer=str)
    category = scrapy.Field(serializer=str)
    price = scrapy.Field(serializer=float)
    product_d = scrapy.Field(serializer=str)
    pack_size = scrapy.Field(serializer=str)
    manufacturer_address = scrapy.Field(serializer=str)
    return_address = scrapy.Field(serializer=str)
    net_contents = scrapy.Field(serializer=str)
    review = scrapy.Field(serializer=list)
    next_products = scrapy.Field(serializer=list)

class tesco_item_review(scrapy.Item):
    review_title = scrapy.Field(serializer=str)
    stars_count = scrapy.Field(serializer=int)
    author = scrapy.Field(serializer=str)
    date = scrapy.Field(serializer=str)
    review_text = scrapy.Field(serializer=str)

class tesco_item_next(scrapy.Item):
    product_url_next = scrapy.Field(serializer=str)
    product_title_next = scrapy.Field(serializer=str)
    image_url_next = scrapy.Field(serializer=str)
    price_next = scrapy.Field(serializer=float)