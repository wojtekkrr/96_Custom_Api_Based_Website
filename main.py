from flask import Flask, render_template, url_for, request, redirect
import requests
import os
from pprint import pprint

api_key = os.environ['Weather_App_Key']

url = "https://api.openweathermap.org/data/2.5/forecast"

url_longitude_latitude = "https://geocode.maps.co/search?q="

app = Flask(__name__)

city_names = None

city = None

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        global city_names
        global city
        place = request.form

        response = requests.get(url=url_longitude_latitude + place["city"])

        city = response.json()

        city_names = []
        for i in range(6):
            city_names.append(city[i]["display_name"])

        # Numeracja miast
        numbered_cities = [(index, city_name) for index, city_name in enumerate(city_names)]

        metoda = "post"

        return render_template("index.html", city_names=numbered_cities, metoda=metoda)

    metoda = "get"
    return render_template("index.html", metoda=metoda)


@app.route("/city/<int:city_id>")
def show_city(city_id):
    city_name = city[city_id]["display_name"]
    MY_LAT = city[city_id]["lat"]
    MY_LONG = city[city_id]["lon"]

    parameters = {
        "lat": MY_LAT,
        "lon": MY_LONG,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(url=url, params=parameters)

    data = response.json()

    bring_umbrella = False
    for i in range(8):
        if data["list"][i]["weather"][0]["id"] < 700:
            bring_umbrella = True

    return render_template("weather.html", city_name=city_name, umbrela=bring_umbrella)


if __name__ == "__main__":
    app.run(debug=True, port=5010)
