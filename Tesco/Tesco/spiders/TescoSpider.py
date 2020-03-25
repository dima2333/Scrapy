import json
import time
import math
import scrapy

from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from Tesco.items import tesco_item, tesco_item_review, tesco_item_next
import openpyxl


class TescospiderSpider(scrapy.Spider):
    name = 'TescoSpider'
    allowed_domains = ['tesco.com']
    item_rlist = []

    def start_requests(self):
        # try:
        #   eBuffer = openpyxl.load_workbook('Quest_Links_for_the_Tesco_com_parser2.xlsx')
        #   list1 = eBuffer.get_sheet_by_name('Лист1')
        #   urls_list = []
        #   for i in range(1, 3):
        #       urls_list.append(list1.cell(row=i, column=1).value)274447328 302664282 271374384
        # except Exception as e:
        #   print("Error : ", e)
        urls_list = [
            'https://www.tesco.com/groceries/en-GB/products/302664282']
        for url in urls_list:
            yield scrapy.Request(url=url, callback=self.parse_review)

    def parse_review(self, response):
        root = Selector(response)
        SET_SELECTOR = root.xpath(
            '//div[contains(@class,"grocery-product__main-col")]')
        item = tesco_item()
        for i in SET_SELECTOR:
            item['product_url'] = i.xpath(
                './/ancestor::body[@id="data-attributes"]/preceding-sibling::head/link[@rel="canonical"]/@href').get(default=""),
            item['product_id'] = i.xpath(
                './/ancestor::body[@id="data-attributes"]/preceding-sibling::head/link[@rel="canonical"]/@href').get(default=0)[-9:],
            item['image_url'] = i.xpath(
                './/div[@class="product-details-tile__main"]//img/@src').get(default=""),
            item['product_title'] = i.xpath(
                './/h1[@class="product-details-tile__title"]/text()').get(default=""),
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
            try:
                count_nodes_next = i.xpath(
                    'count(//div[@class="recommender__wrapper"]/div[@class="product-tile-wrapper"])').getall()[0],
                count_nodes_next = int(float(count_nodes_next[0]))
            except Exception as e:
                print("Error : ", e)
                count_nodes_next = 0
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

            # разбираем информацию json в первом ответе от сервера
            data_props_str = response.xpath('//body/@data-props').get()
            data_props_json = json.loads(data_props_str)
            prod_id = data_props_json["resources"]["productDetails"]["data"]["product"]["reviews"]["product"]["tpnb"]
            prod_review_info = data_props_json["resources"]["productDetails"]["data"]["product"]["reviews"]["info"]
            prod_review_entries = data_props_json["resources"][
                "productDetails"]["data"]["product"]["reviews"]["entries"]

            # формирование списка объектов Review (array of objects) из JSON
            item['review'] = []
            for val in prod_review_entries:
                itemr = tesco_item_review()

                # формирование review_title - заголовка отзыва
                if val['summary'] == None:
                    itemr['review_title'] = val['text'][:50] if val['text'] != None else '',
                else:
                    itemr['review_title'] = val['summary'],

                # формирование stars_count - рейтинг звезд
                itemr['stars_count'] = val['rating']['value'],

                # формирование author - автор отзыва
                if val['syndicationSource']['name'] == None:
                    itemr['author'] = 'A Tesco Customer',
                else:
                    itemr['author'] = val['syndicationSource']['name'],

                # формирование data - дата отзыва
                time_val = str(val['submissionTime'])
                tm1 = time.ctime(int(time_val[:10]))
                dt = time.strptime(tm1, '%a %b %d %H:%M:%S %Y')
                itemr['date'] = time.strftime('%dth %B %Y', dt),

                # формирование review_text - тела(текст) отзыва
                if val['text'] == None:
                    itemr['review_text'] = ('',),
                else:
                    itemr['review_text'] = val['text'],
                self.item_rlist.append(itemr)
            item['review'] = self.item_rlist
            self.item_rlist = []
            max_page = math.ceil(
                prod_review_info['total'] / prod_review_info['count']) + 1
            for next_page in range(2, max_page):
                yield scrapy.Request("https://www.tesco.com/groceries/en-GB/reviews/{}?page={}".format(prod_id, next_page), callback=self.parse_item_review, headers={"Content-Type": "application/json", "Accept": "application/json, text/javascript, */*; q=0.01"}, meta={'collected_item': item})
        yield item

    def parse_item_review(self, response):
        self.item_rlist = []
        item = response.meta['collected_item']
        data_props_json = json.loads(response.body)
        data_props_json = data_props_json["entries"]
        for val in data_props_json:
            itemr = tesco_item_review()

            # формирование review_title - заголовка отзыва
            if val['summary'] == None:
                itemr['review_title'] = val['text'][:50] if val['text'] != None else '',
            else:
                itemr['review_title'] = val['summary'],

            # формирование stars_count - рейтинг звезд
            itemr['stars_count'] = val['rating']['value'],
            # формирование author - автор отзыва
            if val['syndicationSource']['name'] == None:
                itemr['author'] = 'A Tesco Customer',
            else:
                itemr['author'] = val['syndicationSource']['name'],

            # формирование data - дата отзыва
            time_val = str(val['submissionTime'])
            tm1 = time.ctime(int(time_val[:10]))
            dt = time.strptime(tm1, '%a %b %d %H:%M:%S %Y')
            itemr['date'] = time.strftime('%dth %B %Y', dt),

            # формирование review_text - тела(текст) отзыва
            if val['text'] == None:
                itemr['review_text'] = ('',),
            else:
                itemr['review_text'] = val['text'],
            self.item_rlist.append(itemr)
        item['review'] = self.item_rlist
        self.item_rlist = []
        yield item