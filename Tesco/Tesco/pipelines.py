# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

class TescoPipeline(object):
    def process_item(self, item, spider):
        item['ProductURL']          = item['ProductURL'][0]
        item['ProductID']           = item['ProductID'][0]
        item['ImageURL']            = item['ImageURL'][0]
        item['ProductTitle']        = item['ProductTitle'][0]
        item['Category']            = item['Category'][0]
        item['Price']               = item['Price'][0]
        
        ProductD = ''
        listD    = item['ProductD'][0]
        for i in range(0, len(listD)):
            ProductD += listD[i] + ' '
        item['ProductD']            = ProductD
        
        item['PackSize']            = item['PackSize'][0]
        
        ManufacturerAddress = ''
        for i in item['ManufacturerAddress'][0]:
            ManufacturerAddress += i + ' '
        item['ManufacturerAddress'] = ManufacturerAddress

        ReturnAddress = ''
        for i in item['ReturnAddress'][0]:
            ReturnAddress += i + ' '
        item['ReturnAddress']       = ReturnAddress
        
        item['NetContents']         = item['NetContents'][0]

        for i in item['Review']:
            i['ReviewTitle']        = i['ReviewTitle'][0]
            s                       = i['StarsCount'][0]
            l                       = s.find('stars')
            i['StarsCount']         = int(s[:l])
            i['Author']             = i['Author'][0]
            i['Date']               = i['Date'][0]
            i['ReviewText']         = i['ReviewText'][0]

        for j in item['NextProducts']:
            j['ProductURLNext']     = str('https://www.tesco.com' + j['ProductURLNext'][0])
            j['ProductTitleNext']   = j['ProductTitleNext'][0]
            j['ImageURLNext']       = j['ImageURLNext'][0]
            j['PriceNext']          = float(j['PriceNext'][0])
        return item