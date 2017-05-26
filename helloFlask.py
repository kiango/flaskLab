from flask import Flask, render_template, request
import data_processing
import time
import requests
import re
import operator
import urllib3

# --------- CONSTANTS ---------
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


app = Flask(__name__)
url_shoes = 'https://www.unisport.dk/api/sample/'
http = urllib3.PoolManager()


def get_http_status_code():
    response = http.request('GET', url_shoes)
    http_status_code = str(response.status)
    return http_status_code


fresh_json = ''
time_of_json_request = 0


# getting data from API, register the time method call,
# sort data by data_processing.data_sorter(fresh_json)
# and save the data in global variable
def get_json_object():
    global time_of_json_request
    time_of_json_request = time.time()
    response_shoes = requests.get(url_shoes)
    global fresh_json
    fresh_json = response_shoes.json()
    data_processing.data_sorter(fresh_json)
    return fresh_json


@app.route('/get_product', methods=['GET'])
def get_product():
    message = 'no match!'
    get_product_time = time.time()

    # validate input
    product_id = request.args.get('get_data')
    if not re.match("^[0-9]{1,6}$", product_id):
        return render_template('product.html', pid=product_id, msg=message)
    elif (get_product_time - time_of_json_request) > 3600:
        product_spec = []
        json_object_shoes = get_json_object()
        # alternative item retrieval gets updated json data
        # for i, value in enumerate(json_object_shoes['products']):
        #     if json_object_shoes['products'][i]['id'] == product_id:
        #         print(json_object_shoes['products'][i])
        #         product_spec.append(json_object_shoes['products'][i])
        #     # print(json_object_shoes['products'][i]['id'])
        #         return render_template('product.html', pid=product_id, ps=product_spec)
        #         break

        for products in json_object_shoes['products']:
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
                return render_template('product.html', pid=product_id, ps=product_spec)
                break
        return render_template('product.html', pid=product_id, msg=message)
    else:
        product_spec = []
        json_object_shoes = fresh_json

        for products in json_object_shoes['products']:
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
                return render_template('product.html', pid=product_id, ps=product_spec)
                break
        return render_template('product.html', pid=product_id, msg=message)


@app.route('/get_kids_items', methods=['GET'])
def get_kids_items():
    json_object_shoes = get_json_object()

    kids_product_msg = 'No kids products'
    products_kids = []
    price_kids = []

    for products in json_object_shoes['products']:
        if products['kids'] != "1":
            return render_template('kids.html', kmsg=kids_product_msg)
        elif products['kids'] == "1":
            products_kids.append(products['name'])
            price_kids.append(products['price'].replace(',', '.'))

    price_kids = [float(i) for i in price_kids]  # convert string to float

    # build dictionary of product name and price lists, sort by dictionary value (lowest price first)
    kids_product_price = dict(zip(products_kids, price_kids))
    kids_product_price = sorted(kids_product_price.items(), key=operator.itemgetter(1))
    return render_template('kids.html', kpp=kids_product_price)


product_price = {}
client_product_request_time = 0
http_status_msg_ok = 'Connection is OK!'
http_status_msg_bad = 'Connection is Bad!'


@app.route('/get_products')
def get_products():
    global client_product_request_time
    global http_status_msg_ok
    global http_status_msg_bad
    client_product_request_time = time.time()

    # don't get data if client server connection is bad
    if get_http_status_code() != '200':
        return render_template('get_products.html', msg=http_status_msg_bad)

    # get a new json if json data is old (3600 seconds)
    elif (client_product_request_time - time_of_json_request) > 3600:

        json_object_shoes = get_json_object()

        # Get only product name and product price from json data
        # product_list = []
        # price_list = []
        # for products in json_object_shoes['products']:
        #     product_list.append(products['name'])
        #     price_list.append(products['price'].replace(',', '.'))

        # Pagination:
        # retrieve url-variable value of 'skip'
        page = request.args.get('skip')
        if page is None:
            page = '0'
        page = int(page)  # cast
        pagination_size = 5
        # array index for pagination slices
        start_index = page * pagination_size
        end_index = start_index + pagination_size

        all_products = json_object_shoes['products']
        paginated_data = all_products[start_index: end_index]

        # sorting by price in list:
        # price_list = [float(i) for i in price_list]  # convert string price to float
        # build dictionary of product name and price sort by dictionary value (lowest price)
        # product_price = dict(zip(product_list, price_list))
        # product_price = sorted(product_price.items(), key=operator.itemgetter(1))

        return render_template('get_products.html',
                               data=paginated_data,
                               length=len(all_products),
                               msg=http_status_msg_ok)

    else:  # get cached json if json data is not too old

        json_object_shoes = fresh_json

        # retrieve url-variable value of 'skip'
        page = request.args.get('skip')
        if page is None:
            page = '0'
        page = int(page)  # cast
        pagination_size = 5

        # array index for pagination slices
        start_index = page * pagination_size
        end_index = start_index + pagination_size

        all_products = json_object_shoes['products']
        paginated_data = all_products[start_index: end_index]

        return render_template('get_products.html',
                               data=paginated_data,
                               length=len(all_products),
                               msg=http_status_msg_ok)


@app.route('/shoes', methods=['GET'])
def shoes():
    get_json_object()  # getting json data before client request for caching
    return render_template('shoes.html')


@app.route('/temperature', methods=['POST'])
def temperature():
    city = request.form['City']
    # url_latlon= 'http://api.openweathermap.org/data/2.5/weather?lat=35&lon=100&appid=d17bac13d9616e1dd429b0c03e869997'
    url_city = 'http://api.openweathermap.org/data/2.5/weather?q='+city+',dk&appid=d17bac13d9616e1dd429b0c03e869997'
    response = requests.get(url_city)
    json_object = response.json()
    temp_kelvin = float(json_object['main']['temp'])
    temp_celsius = round(temp_kelvin - 273, 1)

    lon = json_object['coord']['lon']
    lat = json_object['coord']['lat']
    return render_template('temperature.html',
                           city=city,
                           temp=temp_celsius,
                           lon=lon,
                           lat=lat)  # return temperature + temperature.html


@app.route('/geography')
def geography():
    geographic_setting = ["C: coastline", "D: desert", "M: mountain", "O: ocean"]
    return render_template('geography.html', geographic_setting=geographic_setting)


@app.route('/profile/<profile_name>')
def profile(profile_name):
    return render_template('profile.html', profile_name=profile_name)


# @ indicates a decorator a way to wrap a function and modify its behavior
# app.route(...) maps a url to a function in this case this return value
# here we have 2 url's binded to the same return object
@app.route('/<weather>')
@app.route('/')
def index(weather=None):
    return render_template('index.html', weather=weather)

# start the web server directly in debug mode
if __name__ == "__main__":
    app.run(debug=True)
