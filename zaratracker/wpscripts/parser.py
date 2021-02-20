import requests
import json

class ReferenceParser:

    def __init__(self, url, reference_obj):
        self.url = url
        self.reference_obj = reference_obj

    def get_reference_data_set(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        }
        response_dict = json.loads(requests.get(self.url, headers=headers).text)
        productGroups_list = response_dict['productGroups']

        data_set = []
        for productGroup in productGroups_list:
            elements_list = productGroup['elements']
            for element in elements_list:
                commercialComponents_list = element['commercialComponents']
                for component in commercialComponents_list:
                    data = {}
                    if str(component['id']).isdigit() and len(str(component['id'])) == 8:
                        
                        #BUNDLES
                        if component['type'] == 'Bundle':
                            try:
                                try:
                                    bundle_list = component['bundleProducts']
                                    bundleProducts = []
                                    for item in bundle_list:
                                        bundle_item = {}
                                        bundle_item['id'] = item['id']
                                        bundle_item['name'] = item['name']
                                        bundle_item['price'] = str(int(item['price'])/100)
                                        try:
                                            bundle_item['oldPrice'] = str(int(item['oldPrice'])/100)
                                        except KeyError:
                                            bundle_item['oldPrice'] = 'no_sale'

                                        bundleProducts.append(bundle_item)

                                    data['bundleProducts'] = bundleProducts
                                except KeyError:
                                    continue
                                data['id'] = component['id']
                                data['type'] = component['type']
                                data['name'] = component['name']
                                data['product_url'] = self.create_product_url(component['seo'])
                                try:
                                    data['product_image_url'] = self.create_product_image_url(component['simpleXmedia'][0])
                                except IndexError:
                                    data['product_image_url'] = ''
                                data['currency'] = self.reference_obj.region.currency
                                data['price'] = str(int(component['price'])/100)
                                try:
                                    data['oldPrice'] = str(int(component['oldPrice'])/100)
                                except KeyError:
                                    data['oldPrice'] = 'no_sale'
                                try:
                                    data['isOnSale'] = component['isOnSale']
                                except KeyError:
                                    data['isOnSale'] = 'false'

                                data_set.append(data)
                            except KeyError:
                                continue

                        #PRODUCTS
                        elif component['type'] == 'Product':
                            data['id'] = component['id']
                            data['type'] = component['type']
                            data['name'] = component['name']
                            data['availability'] = component['availability']
                            data['product_url'] = self.create_product_url(component['seo'])
                            data['product_image_url'] = self.create_product_image_url(component['simpleXmedia'][0])
                            data['currency'] = self.reference_obj.region.currency
                            try:
                                data['price'] = str(int(component['price'])/100)
                            except KeyError:
                                data['price'] = 'unknown'
                            
                            try:
                                data['oldPrice'] = str(int(component['oldPrice'])/100)
                            except KeyError:
                                data['oldPrice'] = 'no_sale'
                            if data['oldPrice'] != 'no_sale':
                                sale_counter = str(int(100 - 100 * float(data['price']) / float(data['oldPrice']))) + '%'
                                data['sale_counter'] = sale_counter

                            try:
                                data['isOnSale'] = component['isOnSale']
                            except KeyError:
                                data['isOnSale'] = 'false'

                            data_set.append(data)

        return data_set
    
    def create_product_url(self, seo):
        host = 'https://www.zara.com/'
        region = self.reference_obj.region.shortcut
        language = '/en/'
        keyword = seo['keyword']
        seoProductId = '-p' + seo['seoProductId'] + '.html'
        product_url = host + region + language + keyword + seoProductId

        return str(product_url)

    def create_product_image_url(self, xmedia):
        host = 'https://static.zara.net/photos//'
        path = xmedia['path']
        name = '/' + xmedia['name'] + '.jpg'
        timestamp = '?ts=' + xmedia['timestamp']
        url = host + path + name + timestamp

        return url

