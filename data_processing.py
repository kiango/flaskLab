import locale
from operator import itemgetter

''' 
Sorting a dictionary type by price through
converting from local currency to float,
sorting and converting back to local currency (DKK)
'''


def data_sorter(dict_data):
    # set local data formatting for DK
    locale.setlocale(locale.LC_ALL, "en_DK.utf8")

    # DKK currency to float conversion
    for i in dict_data['products']:
        i['price'] = locale.atof(i['price'])
        # print(i['price'])

    # print(dict_price['products'][0]['price'])  # get price element

    # SORTING DICTIONARY by PRICE
    dict_data['products'].sort(key=itemgetter('price'))
    # for q in dict_price['products']:
    #    print(q['price'])

    # convert float to back to DKK currency
    for k in dict_data['products']:
        k['price'] = locale.currency(k['price'], grouping=True)  # comma & 2 decimals & thousand separation
        k['price'] = k['price'][3:]  # strip the first 3 characters ('kr ') of the generated price values

    # ------   inspection --------
    # for q in dict_data['products']:
    #     print(q['price'], q['name'])

    return dict_data


# --------- ITEM ATTRIBUTE CONSTANTS ---------
NAME = 'name: '
SIZES = 'sizes: '
IS_CUSTOMIZABLE = 'is_customizable: '
DELIVERY = 'delivery: '
KIDS = 'kids: '
KID_ADULT = 'kid_adult: '
FREE_PORTO = 'free_porto: '
IMAGE = 'image: '
PACKAGE = 'package: '
PRICE = 'price: '
URL = 'url: '
ONLINE = 'online: '
PRICE_OLD = 'price_old: '
CURRENCY = 'currency: '
IMG_URL = 'img_url: '
ID = 'id: '
WOMEN = 'women: '


def get_product_spec(product_id, dict_data):
    product_spec = []
    for products in dict_data['products']:
        if products['id'] == product_id:
            product_spec.append(NAME + products['name'])
            product_spec.append(SIZES + products['sizes'])
            product_spec.append(IS_CUSTOMIZABLE + products['is_customizable'])
            product_spec.append(DELIVERY + products['delivery'])
            product_spec.append(KIDS + products['kids'])
            product_spec.append(KID_ADULT + products['kid_adult'])
            product_spec.append(FREE_PORTO + products['free_porto'])
            product_spec.append(IMAGE + products['image'])
            product_spec.append(PACKAGE + products['package'])
            product_spec.append(PRICE + products['price'])
            product_spec.append(URL + products['url'])
            product_spec.append(ONLINE + products['online'])
            product_spec.append(PRICE_OLD + products['price_old'])
            product_spec.append(CURRENCY + products['currency'])
            product_spec.append(IMG_URL + products['img_url'])
            product_spec.append(ID + products['id'])
            product_spec.append(WOMEN + products['women'])

    return product_spec

