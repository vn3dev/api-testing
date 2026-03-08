import requests

url = "https://api.open-meteo.com/v1/forecast?latitude=-10.83&longitude=-63.34&hourly=temperature_2m&forecast_days=1"

response = requests.get(url)
data = response.json()

print(data)