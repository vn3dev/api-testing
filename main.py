import json
import requests
from datetime import datetime

with open("municipios.json", "r", encoding="utf-8-sig") as arquivo:
    municipios = json.load(arquivo)

nome_busca = input("nome do municipio: ").strip().lower()

municipio_encontrado = None

for municipio in municipios:
    if municipio["nome"].lower() == nome_busca:
        municipio_encontrado = municipio
        break

if municipio_encontrado:
    lat = municipio_encontrado["latitude"]
    lon = municipio_encontrado["longitude"]

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&forecast_days=1&timezone=auto"
    response = requests.get(url)
    data = response.json()

    hora_atual = datetime.now().strftime("%Y-%m-%dT%H:00")
    times = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]

    if hora_atual in times:
        indice = times.index(hora_atual)
        temperatura = temps[indice]

        print(f"municipio: {municipio_encontrado['nome']}")
        print(f"temp atual: {temperatura} C")
    else:
        print("nao encontrado")
else:
    print("nao encontrado")