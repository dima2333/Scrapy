import logging

class TescoPipeline(object):
    def process_item(self, item, spider):
        try:
            item['product_url'] = item['product_url'][0]
        except Exception as e:
            logging.info('Error in [product_url] : %s', e)
            item['product_url'] = ''
        try:
            item['product_id'] = item['product_id'][0]
        except Exception as e:
            logging.info('Error in [product_id] : %s', e)
            item['product_id'] = 0
        try:
            item['image_url'] = item['image_url'][0]
        except Exception as e:
            logging.info('Error in [image_url] : %s', e)
            item['image_url'] = ''
        try:
            item['product_title'] = item['product_title'][0]
        except Exception as e:
            logging.info('Error in [product_title] : %s', e)
            item['product_title'] = ''
        try:
            item['category'] = item['category'][0]
        except Exception as e:
            logging.info('Error in [category] : %s', e)
            item['category'] = ''
        try:
            item['price'] = item['price'][0]
        except Exception as e:
            logging.info('Error in [price] : %s', e)
            item['price'] = 0.0
        try:
            product_d = ''
            list_d = item['product_d'][0]
            for i in range(0, len(list_d)):
                product_d += list_d[i] + ' '
            item['product_d'] = product_d
        except Exception as e:
            logging.info('Error in [product_d] : %s', e)
            item['product_d'] = ''
        try:
            item['pack_size'] = item['pack_size'][0]
        except Exception as e:
            logging.info('Error in [pack_size] : %s', e)
            item['pack_size'] = ''
        try:
            manufacturer_address = ''
            for i in item['manufacturer_address'][0]:
                manufacturer_address += i + ' '
            item['manufacturer_address'] = manufacturer_address
        except Exception as e:
            logging.info('Error in [manufacturer_address] : %s', e)
            item['manufacturer_address'] = ''
        try:
            return_address = ''
            for i in item['return_address'][0]:
                return_address += i + ' '
            item['return_address'] = return_address
        except Exception as e:
            logging.info('Error in [return_address] : %s', e)
            item['return_address'] = ''
        try:
            item['net_contents'] = item['net_contents'][0]
        except Exception as e:
            logging.info('Error in [net_contents] : %s', e)
            item['net_contents'] = ''
        
        for i in item['review']:
            i['review_title'] = i['review_title'][0]
            i['stars_count'] = i['stars_count'][0]
            i['author'] = i['author'][0]
            i['date'] = i['date'][0]
            i['review_text'] = i['review_text'][0]

        for j in item['next_products']:
            j['product_url_next'] = str('https://www.tesco.com' + j['product_url_next'][0])
            j['product_title_next'] = j['product_title_next'][0]
            j['image_url_next'] = j['image_url_next'][0]
            j['price_next'] = float(j['price_next'][0])
        return item