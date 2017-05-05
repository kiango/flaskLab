from flask import Flask, render_template, request

from pprint import pprint
import requests
import re
import operator
import urllib3


app = Flask(__name__)
url_shoes = 'https://www.unisport.dk/api/sample/'
http = urllib3.PoolManager()


def get_http_status_code():
    response = http.request('GET', url_shoes)
    http_status_code = str(response.status)
    return http_status_code


# retrieve and return json object
def get_json_object():
    response_shoes = requests.get(url_shoes)
    return response_shoes.json()


@app.route('/get_product', methods=['GET'])
def get_product():
    message = 'no match!'
    product_spec = ''

    # validate input first
    product_id = request.args.get('get_data')
    if not re.match("^[0-9]{6}$", product_id):
        return render_template('product.html', pid=product_id, msg=message)
    else:
        json_object_shoes = get_json_object()
        for products in json_object_shoes['products']:
            if products['id'] == product_id:
                product_spec = products
                return render_template('product.html', pid=product_id, ps=product_spec)
            else:
                return render_template('product.html', pid=product_id, msg=message)


@app.route('/get_kids_items', methods=['GET'])
def get_kids_items():
    json_object_shoes = get_json_object()

    products_kids = []
    price_kids = []

    for products in json_object_shoes['products']:
        if products['kids'] == "1":
            products_kids.append(products['name'])
            price_kids.append(products['price'].replace(',', '.'))

    price_kids = [float(i) for i in price_kids]  # convert string to float

    # build dictionary of product name and price, sort by dictionary value (lowest price)
    kids_product_price = dict(zip(products_kids, price_kids))
    kids_product_price = sorted(kids_product_price.items(), key=operator.itemgetter(1))
    return render_template('kids.html', kpp=kids_product_price)


@app.route('/get_products')
def get_products():
    http_status_msg_bad = 'bad connection to server!'
    http_status_msg_ok = 'Connection OK'

    if get_http_status_code() != '200':
        return render_template('get_products.html', msg=http_status_msg_bad, pp=['??'])
    else:
        json_object_shoes = get_json_object()
        product_list = []
        price_list = []
        for products in json_object_shoes['products']:
            product_list.append(products['name'])
            price_list.append(products['price'].replace(',', '.'))

        price_list = [float(i) for i in price_list]  # convert string price to float
        # build dictionary of product name and price sort by dictionary value (lowest price)
        product_price = dict(zip(product_list, price_list))
        product_price = sorted(product_price.items(), key=operator.itemgetter(1))

        return render_template('get_products.html', msg=http_status_msg_ok, pp=product_price)


@app.route('/shoes', methods=['GET'])
def shoes():
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
@app.route('/')
def index():
    return render_template('index.html')

# start the web server directly in debug mode
if __name__ == "__main__":
    app.run(debug=True)
