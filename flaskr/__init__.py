#!/usr/bin/python3
# -*- coding: latin-1 -*-
import os
import sys
# import psycopg2
import json
from bson import json_util
from pymongo import MongoClient
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify


def create_app():
    app = Flask(__name__)
    return app

app = create_app()

# REPLACE WITH YOUR DATABASE NAME
MONGODATABASE = "myDataBase"
MONGOSERVER = "localhost"
MONGOPORT = 27017
client = MongoClient(MONGOSERVER, MONGOPORT)
mongodb = client[MONGODATABASE]

''' # Uncomment for postgres connection
# REPLACE WITH YOUR DATABASE NAME, USER AND PASS
POSTGRESDATABASE = "mydatabase"
POSTGRESUSER = "myuser"
POSTGRESPASS = "mypass"
postgresdb = psycopg2.connect(
    database=POSTGRESDATABASE,
    user=POSTGRESUSER,
    password=POSTGRESPASS)
'''

#Cambiar por Path Absoluto en el servidor
QUERIES_FILENAME = 'var/www/flaskr/queries'


@app.route("/")
def home():
    with open(QUERIES_FILENAME, 'r', encoding='utf-8') as queries_file:
        json_file = json.load(queries_file)
        pairs = [(x["name"],
                  x["database"],
                  x["description"],
                  x["query"]) for x in json_file]
        return render_template('file.html', results=pairs)


@app.route("/mongo")
def mongo():
    query = request.args.get("query")
    results = eval('mongodb.'+query)
    results = json_util.dumps(results, sort_keys=True, indent=4)
    if "find" in query:
        return render_template('mongo.html', results=results)
    else:
        return "ok"


@app.route("/postgres")
def postgres():
    query = request.args.get("query")
    cursor = postgresdb.cursor()
    cursor.execute(query)
    results = [[a for a in result] for result in cursor]
    print(results)
    return render_template('postgres.html', results=results)


@app.route("/example")
def example():
    return render_template('example.html')

@app.route("/api/date")
def messages_by_date():
    date = request.args.get("date")
    resultado = []
    for mensaje in data:
        if date == mensaje["fecha"]:
            resultado.append(mensaje)
    return jsonify(resultado)

@app.route("/api/ultimos")
def ultimos_mensajes():
    numero = request.args.get("numero")
    k = request.args.get("k")
    resultado = []
    for mensaje in data:
        if numero == mensaje["numero"]:
            resultado.append(mensaje)
    resultado.sort(key=lambda k: k["fecha"], reverse=True)
    try:
        if len(resultado) > int(k):
            resultado = resultado[:int(k)]
    except ValueError:
        pass        
    return jsonify(resultado)

@app.route("/api/clave")
def palabra_clave():
    keyword = request.args.get("keyword")
    resultado = []
    for mensaje in data:
        if keyword.lower() in mensaje["contenido"].lower():
            resultado.append(mensaje)
    return jsonify(resultado)

with open("var/www/flaskr/escuchas.json", encoding='utf-8') as file:
    data = json.load(file)
    


if __name__ == "__main__":
    app.run()
