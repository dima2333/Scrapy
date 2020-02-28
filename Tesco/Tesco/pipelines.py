class tesco_pipeline(object):
    def process_item(self, item, spider):
        item['product_url'] = item['product_url'][0]
        item['product_id'] = item['product_id'][0]
        item['image_url'] = item['image_url'][0]
        item['product_title'] = item['product_title'][0]
        item['category'] = item['category'][0]
        item['price'] = item['price'][0]

        product_d = ''
        list_d = item['product_d'][0]
        for i in range(0, len(list_d)):
            product_d += list_d[i] + ' '
        item['product_d'] = product_d

        item['pack_size'] = item['pack_size'][0]

        manufacturer_address = ''
        for i in item['manufacturer_address'][0]:
            manufacturer_address += i + ' '
        item['manufacturer_address'] = manufacturer_address

        return_address = ''
        for i in item['return_address'][0]:
            return_address += i + ' '
        item['return_address'] = return_address

        item['net_contents'] = item['net_contents'][0]

        for i in item['review']:
            i['review_title'] = i['review_title'][0]
            if type(i['stars_count']) == int:
                i['stars_count'] = i['stars_count']
            else:
                s = i['stars_count'][0]
                l = s.find('stars')
                i['stars_count'] = int(s[:l])
            i['author'] = i['author'][0]
            i['date'] = i['date'][0]
            i['review_text'] = i['review_text'][0]

        for j in item['next_products']:
            j['product_url_next'] = str(
                'https://www.tesco.com' + j['product_url_next'][0])
            j['product_title_next'] = j['product_title_next'][0]
            j['image_url_next'] = j['image_url_next'][0]
            j['price_next'] = float(j['price_next'][0])
        return item