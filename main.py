import json
import requests

with open("municipios.json", "r", encoding="utf-8-sig") as arq:
    municipios = json.load(arq)

with open("estados.json", "r", encoding="utf-8-sig") as arq:
    estados = json.load(arq)

nome_municipio = input("digite o municipio: ").strip().lower()
uf_digitada = input("digite a UF: ").strip().upper()

codigo_uf = None

for estado in estados:
    if estado["uf"].upper() == uf_digitada:
        codigo_uf = estado["codigo_uf"]
        break

if codigo_uf is None:
    print("UF n encontrada")
else:
    municipio_encontrado = None

    for municipio in municipios:
        if municipio["nome"].lower() == nome_municipio and municipio["codigo_uf"] == codigo_uf:
            municipio_encontrado = municipio
            break

    if municipio_encontrado:
        lat = municipio_encontrado["latitude"]
        lon = municipio_encontrado["longitude"]

        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&forecast_days=1&timezone=auto&current_weather=true"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            print(f"Erro ao consultar a API: {e}")
            exit()

        hora_atual = data["current_weather"]["time"]
        times = data["hourly"]["time"]
        temps = data["hourly"]["temperature_2m"]

        if hora_atual in times:
            indice = times.index(hora_atual)
            temperatura = temps[indice]

            print(f"\nmunicipio: {municipio_encontrado['nome']} - {uf_digitada}")
            print(f"lat: {lat}")
            print(f"lon: {lon}")
            print(f"temp atual: {temperatura} C")
        else:
            print("nao encontrado")
    else:
        print("municio não encontrado nessa UF")