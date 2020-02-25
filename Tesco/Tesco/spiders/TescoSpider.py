# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from Tesco.items import tesco_item, tesco_item_review, tesco_item_next
import openpyxl

eBuffer = openpyxl.load_workbook('Quest_Links_for_the_Tesco_com_parser.xlsx')
list1 = eBuffer.get_sheet_by_name('Лист1')
urls_list = []
for i in range(1, 101):
    urls_list.append(list1.cell(row=i, column=1).value)

class TescospiderSpider(scrapy.Spider):
    name = 'TescoSpider'
    allowed_domains = ['tesco.com']
    #start_urls = urls_list[:]
    # 301947168 302664282
    start_urls = ['https://www.tesco.com/groceries/en-GB/products/302664282']

    def parse(self, response):
        #print("RESPONSE URL 1 :", response.url)
        root = Selector(response)
        SET_SELECTOR = root.xpath(
            '//div[contains(@class,"grocery-product__main-col")]')

        for i in SET_SELECTOR:
            item = tesco_item()
            item['product_url'] = i.xpath(
                './/ancestor::body[@id="data-attributes"]/preceding-sibling::head/link[@rel="canonical"]/@href').get(default=""),
            item['product_id'] = i.xpath(
                './/ancestor::body[@id="data-attributes"]/preceding-sibling::head/link[@rel="canonical"]/@href').get(default=0)[-9:],
            item['image_url'] = i.xpath(
                './/div[@class="product-details-tile__main"]//img/@src').get(default=""),
            item['product_title'] = i.xpath(
                './/div[@class="product-details-tile__title-wrapper"]/h1/text()').get(default=""),
            item['category'] = i.xpath(
                './/div[@class="grocery-product__related-links"]//span[contains(@class,"button")]/text()').get(default="")[9:],
            item['price'] = i.xpath(
                './/div[contains(@class,"control-wrapper")]//span[@data-auto="price-value"][1]/text()').get(default="0.0"),
            item['product_d'] = i.xpath(
                './/div[@class="product-blocks"]/div[@id="product-description"]/ul/li/text()').getall(),
            item['pack_size'] = i.xpath(
                './/div[@class="product-blocks"]//li[contains(text(),"Pack")]/text()').get(default="")[11:],
            item['manufacturer_address'] = i.xpath(
                './/div[@class="product-blocks"]//div[@id="manufacturer-address"]/ul/li/text()').getall(),
            item['return_address'] = i.xpath(
                './/div[@class="product-blocks"]//div[@id="return-address"]/ul/li/text()').getall(),
            item['net_contents'] = i.xpath(
                './/div[@class="product-blocks"]//div[@id="net-contents"]/p/text()').get(default=""),
            # формирование списка объектов Usually Bought Next Products (array of objects)
            count_nodes_next = i.xpath(
                'count(//div[@class="recommender__wrapper"]/div[@class="product-tile-wrapper"])').getall()[0],
            count_nodes_next = int(float(count_nodes_next[0]))
            item_rlist_next = []
            for index in range(0, count_nodes_next):
                itemn = tesco_item_next()
                itemn['product_url_next'] = SET_SELECTOR.xpath(
                    '//div[@class="recommender__wrapper"]/div[@class="product-tile-wrapper"]/descendant::a[@data-auto="product-tile--title"]/@href').getall()[index],
                itemn['product_title_next'] = SET_SELECTOR.xpath(
                    '//div[@class="recommender__wrapper"]/div[@class="product-tile-wrapper"]//a[@data-auto="product-tile--title"]/text()').getall()[index],
                itemn['image_url_next'] = SET_SELECTOR.xpath(
                    '//div[@class="recommender__wrapper"]/div[@class="product-tile-wrapper"]//img/@src').getall()[index],
                itemn['price_next'] = SET_SELECTOR.xpath(
                    '//div[@class="recommender__wrapper"]/div[@class="product-tile-wrapper"]//form//div[@class="price-control-wrapper"]//span[@data-auto="price-value"]/text()').getall()[index],
                item_rlist_next.append(itemn)
            item['next_products'] = item_rlist_next
            # формирование списка объектов Review (array of objects)
            count_nodes = SET_SELECTOR.xpath(
                'count(.//div[@id="review-data"]/article[@class="reviews-list__content"]/article[@class="review"])').get(),
            count_nodes = int(float(count_nodes[0][:2]))
            item_rlist = []
            for index in range(0, count_nodes):
                itemr = tesco_item_review()
                itemr['review_title'] = SET_SELECTOR.xpath(
                    './/article[@class="reviews-list__content"]/descendant::h3/text()').getall()[index],
                itemr['stars_count'] = SET_SELECTOR.xpath(
                    './/article[@class="reviews-list__content"]/descendant::span[contains(@class,"base-components")]/text()').getall()[index],
                itemr['author'] = SET_SELECTOR.xpath(
                    './/article[@class="reviews-list__content"]/descendant::p[@class="review-author"]/span[1]/text()').getall()[index],
                itemr['date'] = SET_SELECTOR.xpath(
                    './/article[@class="reviews-list__content"]/descendant::p[@class="review-author"]/span[@class="review-author__submission-time"]/text()').getall()[index],
                itemr['review_text'] = SET_SELECTOR.xpath(
                    './/article[@class="reviews-list__content"]/descendant::p[@class="review__text"]/text()').getall()[index],
                item_rlist.append(itemr)
            links = LinkExtractor(
                restrict_xpaths='//div[@class="reviews-list__page"]//a[@class]').extract_links(response)
            for L in links:
                new_request = scrapy.Request(L.url)
                yield new_request
            item['review'] = item_rlist
        yield item