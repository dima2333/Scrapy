# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from Tesco.items import TescoItem, TescoItemReview, TescoItemNext
import openpyxl

eBuffer = openpyxl.load_workbook('Quest_Links_for_the_Tesco_com_parser.xlsx')
list1 = eBuffer.get_sheet_by_name('Лист1')
urls_list = []
for i in range(1, 101):
    urls_list.append(list1.cell(row=i, column=1).value)

class TescospiderSpider(scrapy.Spider):
    name = 'TescoSpider'
    allowed_domains = ['tesco.com']
    start_urls = urls_list[:]
    #start_urls = ['https://www.tesco.com/groceries/en-GB/products/302664282']# 301947168 302664282
    
    def parse(self, response):
        print("RESPONSE URL 1 :", response.url)
        root = Selector(response)
        SET_SELECTOR= root.xpath('//div[contains(@class,"grocery-product__main-col")]')
        
        for i in SET_SELECTOR:
            item = TescoItem()        
            item['ProductURL']              = i.xpath('.//ancestor::body[@id="data-attributes"]/preceding-sibling::head/link[@rel="canonical"]/@href').get(default=""),
            item['ProductID']               = i.xpath('.//ancestor::body[@id="data-attributes"]/preceding-sibling::head/link[@rel="canonical"]/@href').get(default=0)[-9:],
            item['ImageURL']                = i.xpath('.//div[@class="product-details-tile__main"]//img/@src').get(default=""),
            item['ProductTitle']            = i.xpath('.//div[@class="product-details-tile__title-wrapper"]/h1/text()').get(default=""),
            item['Category']                = i.xpath('.//div[@class="grocery-product__related-links"]//span[contains(@class,"button")]/text()').get(default="")[9:],
            item['Price']                   = i.xpath('.//div[contains(@class,"controls--wrapper")]//span[@data-auto="price-value"][1]/text()').get(default="0.0"),
            item['ProductD']                = i.xpath('.//div[@class="product-blocks"]/div[@id="product-description"]/ul/li/text()').getall(),
            item['PackSize']                = i.xpath('.//div[@class="product-blocks"]//li[contains(text(),"Pack")]/text()').get(default="")[11:],
            item['ManufacturerAddress']     = i.xpath('.//div[@class="product-blocks"]//div[@id="manufacturer-address"]/ul/li/text()').getall(),
            item['ReturnAddress']           = i.xpath('.//div[@class="product-blocks"]//div[@id="return-address"]/ul/li/text()').getall(),
            item['NetContents']             = i.xpath('.//div[@class="product-blocks"]//div[@id="net-contents"]/p/text()').get(default=""),
            # формирование списка объектов Usually Bought Next Products (array of objects)            
            countNodesNext                  = i.xpath('count(//div[@class="recommender__wrapper"]/div[@class="product-tile-wrapper"])').getall()[0],
            countNodesNext                  = int(float(countNodesNext[0]))
            itemRListNext                   = []
            for index in range(0, countNodesNext):
                itemN = TescoItemNext()
                itemN['ProductURLNext']     = SET_SELECTOR.xpath('//div[@class="recommender__wrapper"]/div[@class="product-tile-wrapper"]/descendant::a[@data-auto="product-tile--title"]/@href').getall()[index],
                itemN['ProductTitleNext']   = SET_SELECTOR.xpath('//div[@class="recommender__wrapper"]/div[@class="product-tile-wrapper"]//a[@data-auto="product-tile--title"]/text()').getall()[index],
                itemN['ImageURLNext']       = SET_SELECTOR.xpath('//div[@class="recommender__wrapper"]/div[@class="product-tile-wrapper"]//img/@src').getall()[index],
                itemN['PriceNext']          = SET_SELECTOR.xpath('//div[@class="recommender__wrapper"]/div[@class="product-tile-wrapper"]//form//div[@class="price-control-wrapper"]//span[@data-auto="price-value"]/text()').getall()[index],
                itemRListNext.append(itemN)
            item['NextProducts']            = itemRListNext
            # формирование списка объектов Review (array of objects)
            countNodes                      = SET_SELECTOR.xpath('count(.//div[@id="review-data"]/article[@class="reviews-list__content"]/article[@class="review"])').get(),
            countNodes                      = int(float(countNodes[0][:2]))
            itemRList                       = []
            for index in range(0, countNodes):
                itemR = TescoItemReview()
                itemR['ReviewTitle']        = SET_SELECTOR.xpath('.//article[@class="reviews-list__content"]/descendant::h3/text()').getall()[index],
                itemR['StarsCount']         = SET_SELECTOR.xpath('.//article[@class="reviews-list__content"]/descendant::span[contains(@class,"base-components")]/text()').getall()[index],
                itemR['Author']             = SET_SELECTOR.xpath('.//article[@class="reviews-list__content"]/descendant::p[@class="review-author"]/span[1]/text()').getall()[index],
                itemR['Date']               = SET_SELECTOR.xpath('.//article[@class="reviews-list__content"]/descendant::p[@class="review-author"]/span[@class="review-author__submission-time"]/text()').getall()[index],
                itemR['ReviewText']         = SET_SELECTOR.xpath('.//article[@class="reviews-list__content"]/descendant::p[@class="review__text"]/text()').getall()[index],
                itemRList.append(itemR)
            links = LinkExtractor(restrict_xpaths='//div[@class="reviews-list__page"]//a[@class]').extract_links(response)
            for L in links:
                new_request = scrapy.Request(L.url)
                yield new_request
            item['Review']                  = itemRList          
        yield item