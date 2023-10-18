from flask import Flask, render_template, url_for, request
import requests
import os
from pprint import pprint

MY_LAT = 52.237049
MY_LONG = 21.017532

api_key = os.environ['Weather_App_Key']

url="https://api.openweathermap.org/data/2.5/forecast"

parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": api_key,
    "units": "metric"
}

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    # if request.method == "POST":
    #     place = request.form




    response = requests.get(url=url, params=parameters)

    data = response.json()

    bring_umbrella = False
    for i in range(8):
        if data["list"][i]["weather"][0]["id"] < 700:
            bring_umbrella = True

    return render_template("index.html", umbrela=bring_umbrella)


if __name__ == "__main__":
    app.run(debug=True, port=5010)
