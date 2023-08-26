import requests
from pprint import pprint
from datetime import datetime

api_key = "4de28938fbf3fffe90a6bfd10c371a9d"

city = input("Enter Your city: ")
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    country = data["sys"]["country"]
    wind = data["wind"]["speed"]
    timezone = data["timezone"]
    sunrise = datetime.utcfromtimestamp(data["sys"]["sunrise"] + timezone).strftime("%d-%m-%Y %H:%M:%S")
    sunset = datetime.utcfromtimestamp(data["sys"]["sunset"] + timezone).strftime("%d-%m-%Y %H:%M:%S")
    temp = round(int(data["main"]["temp"]) - 273.15, 2)
    desc = data["weather"][0]["description"]
    final_data = f"""
        {city}da Ob-Havo:
        Temperatura: {temp} °C
        Shamol tezligi: {wind}m/s
        Respublika qisqa kodi: {country}
        Quyosh chiqishi: {sunrise}
        Quyosh botishi: {sunset} 
    """
    print(final_data)
else:
    print("error")

