import locale
from operator import itemgetter

''' 
Sorting a dictionary type by price through
converting local currency to float,
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
