import requests
import json

from win10toast import ToastNotifier

import sqlite3

API_KEY = '887aaff89bee4fd742287bfd4afa2483'
location = 'Georgia'
URL = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}"
response = requests.get(URL)
print(response.status_code)
print(response.headers)

if response.status_code == 200:
    data = response.json()

    with open("weather_data.json", "w") as file:
        json.dump(data, file, indent=4)

    print("Weather Information")
    print("Location:", data['name'])
    print("Temperature:", data["main"]["temp"])
    print("Description:", data["weather"][0]["description"])

    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    Text = [data["name"], data["main"]["temp"], data["weather"][0]["description"]]
    cursor.execute("""
    create table if not exists weather(location varchar(50), temperature integer, description 
                   varchar(100))""")

    cursor.execute("""
    insert into weather (location, temperature, description) VALUES (?,?,?)""", Text)
    conn.commit()

    toaster = ToastNotifier()
    toaster.show_toast(
        "Weather Update",
        f"Location: {data['name']}\nTemperature: {data['main']['temp']}\nDescription: {data['weather'][0]['description']}",
        duration=10
    )
else:
    print("Error occurred. Status Code:", response.status_code)

