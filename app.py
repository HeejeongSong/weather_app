from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import datetime
import pytz

app = Flask(__name__)

def get_current_datetime_string():
    now = datetime.now(pytz.timezone('Asia/Seoul'))
    return now.strftime("%Y년 %m월 %d일 %p %I시 %M분")

openweathermap_api_key = 'b4616a64063053291a8bdac9a8a6b3e8'
openweathermap_url = 'http://api.openweathermap.org/data/2.5/weather'

cities = {
    "서울": {"lat": 37.5665, "lon": 126.9780},
    "인천": {"lat": 37.4563, "lon": 126.7052},
    "대전": {"lat": 36.3504, "lon": 127.3845},
    "대구": {"lat": 35.8722, "lon": 128.6025},
    "부산": {"lat": 35.1796, "lon": 129.0756},
    "광주": {"lat": 35.1595, "lon": 126.8526},
    "전주": {"lat": 35.8242, "lon": 127.1470},
    "제주": {"lat": 33.4996, "lon": 126.5312},
    "춘천": {"lat": 37.8813, "lon": 127.7298},
    "울릉도": {"lat": 37.4858, "lon": 130.9057}  
}

def forecast(lat, lon):
    try:
        params = {
            'lat': lat,
            'lon': lon,
            'appid': openweathermap_api_key,
            'units': 'metric',
            'lang': 'kr'
        }

        print(f"Requesting weather data for coordinates (lat: {lat}, lon: {lon})")
        res = requests.get(openweathermap_url, params=params)
        res.raise_for_status()
        json_data = res.json()
        print("API response received successfully.")

        weather_data = {
            'tmp': json_data['main']['temp'],
            'hum': json_data['main']['humidity'],
            'sky': json_data['weather'][0]['main'],
            'sky2': json_data['weather'][0]['description']
        }

        print(f"Weather data for (lat: {lat}, lon: {lon}): {weather_data}")
        return weather_data

    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

def format_weather(city, weather_data):
    if not weather_data:
        return f"{city}의 날씨 정보를 가져올 수 없습니다."

    sky_status = {
        'Clear': "맑음",
        'Clouds': "구름많음",
        'Rain': "비",
        'Snow': "눈",
        'Drizzle': "이슬비",
        'Thunderstorm': "뇌우",
        'Mist': "안개"
    }

    sky_desc = weather_data['sky2']

    return {
        'city': city,
        'datetime': get_current_datetime_string(),
        'temperature': f"{weather_data['tmp']}ºC",
        'sky': sky_desc,
        'humidity': f"{weather_data['hum']}%"
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        if not city:
            return render_template('index.html', cities=cities.keys(), error="도시를 선택해주세요.")
        return redirect(url_for('weather', city=city))
    return render_template('index.html', cities=cities.keys())

@app.route('/weather/<city>')
def weather(city):
    lat, lon = cities[city]['lat'], cities[city]['lon']
    weather_data = forecast(lat, lon)
    weather_info = format_weather(city, weather_data)
    return render_template('weather.html', weather_info=weather_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

