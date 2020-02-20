# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class TescoItem(scrapy.Item):
    ProductURL          = scrapy.Field(serializer= str)
    ProductID           = scrapy.Field(serializer= int)
    ImageURL            = scrapy.Field(serializer= str)
    ProductTitle        = scrapy.Field(serializer= str)
    Category            = scrapy.Field(serializer= str)
    Price               = scrapy.Field(serializer= float)
    ProductD            = scrapy.Field(serializer= str)
    PackSize            = scrapy.Field(serializer= str)
    ManufacturerAddress = scrapy.Field(serializer= str)
    ReturnAddress       = scrapy.Field(serializer= str)
    NetContents         = scrapy.Field(serializer= str)
    Review              = scrapy.Field(serializer= list)
    NextProducts        = scrapy.Field(serializer= list)

class TescoItemReview(scrapy.Item):
    ReviewTitle         = scrapy.Field(serializer= str)
    StarsCount          = scrapy.Field(serializer= int)
    Author              = scrapy.Field(serializer= str)
    Date                = scrapy.Field(serializer= str)
    ReviewText          = scrapy.Field(serializer= str)

class TescoItemNext(scrapy.Item):
    ProductURLNext      = scrapy.Field(serializer= str)
    ProductTitleNext    = scrapy.Field(serializer= str)
    ImageURLNext        = scrapy.Field(serializer= str)
    PriceNext           = scrapy.Field(serializer= float)