import json
import requests

with open("municipios.json", "r", encoding="utf-8-sig") as arq:
    municipios = json.load(arq)

with open("estados.json", "r", encoding="utf-8-sig") as arq:
    estados = json.load(arq)

nome_municipio = input("digite o municipio: ").strip().lower()
uf_digitada = input("digite a UF: ").strip().upper()

print("municipio digitado:", repr(nome_municipio))
print("uf digitada:", repr(uf_digitada))

codigo_uf = None

for estado in estados:
    if estado["uf"].upper() == uf_digitada:
        codigo_uf = estado["codigo_uf"]
        print("codigo_uf encontrado:", codigo_uf)
        break

if codigo_uf is None:
    print("UF n encontrada")
else:
    municipio_encontrado = None

    for municipio in municipios:
        if municipio["codigo_uf"] == codigo_uf and municipio["nome"].lower() == nome_municipio:
            municipio_encontrado = municipio
            break

    if municipio_encontrado:
        print("municipio encontrado no json:", municipio_encontrado["nome"])

        lat = municipio_encontrado["latitude"]
        lon = municipio_encontrado["longitude"]

        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}"
            f"&longitude={lon}"
            f"&current=temperature_2m"
            f"&timezone=auto"
        )

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            print(f"Erro ao consultar a API: {e}")
            exit()

        temperatura = data["current"]["temperature_2m"]

        print(f"\nmunicipio: {municipio_encontrado['nome']} - {uf_digitada}")
        print(f"lat: {lat}")
        print(f"lon: {lon}")
        print(f"temp atual: {temperatura} C")
    else:
        print("municio não encontrado nessa UF")