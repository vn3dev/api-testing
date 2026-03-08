import requests
from datetime import datetime

lat = float(input("lat: "))
lon = float(input("lon: "))

url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&forecast_days=1"

response = requests.get(url)
data = response.json()

# hora atual
now = datetime.now().strftime("%Y-%m-%dT%H:00")

times = data["hourly"]["time"]
temps = data["hourly"]["temperature_2m"]

# encontra indice da hora atual
index = times.index(now)

# temperatura correspondente
current_temp = temps[index]

print("temp atual:", current_temp, "C")