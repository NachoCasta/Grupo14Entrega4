import json

with open("escuchas.json", encoding='utf-8') as file:
    data = json.load(file)

resultado = [{"fecha": "2017-01-02"},{"fecha":"2015-01-32"}]
resultado.sort(key=lambda k: k["fecha"], reverse=True)
