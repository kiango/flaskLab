from flask import Flask, render_template, request
import requests


app = Flask(__name__)


@app.route('/temperature', methods=['POST'])
def temperature():
    city = request.form['City']
    url_latlon= 'http://api.openweathermap.org/data/2.5/weather?lat=35&lon=100&appid=d17bac13d9616e1dd429b0c03e869997'
    url_city = 'http://api.openweathermap.org/data/2.5/weather?q='+city+',dk&appid=d17bac13d9616e1dd429b0c03e869997'
    response = requests.get(url_city)
    json_object = response.json()
    temp_kelvin = float(json_object['main']['temp'])
    temp_celsius = round(temp_kelvin - 273, 1)
    # return str(temp_kelvin)  # return only temperature
    return render_template('temperature.html', city=city, temp=temp_celsius)  # return temperature + temperature.html


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
