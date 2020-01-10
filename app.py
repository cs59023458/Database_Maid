#!/usr/bin/env python3
from flask import Flask, request, url_for, jsonify
from flask_api import FlaskAPI, status, exceptions
import paho.mqtt.client as mqttClient
from tinydb import TinyDB, Query
import json
import time

Connected = False


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        global Connected
        Connected = True
    else:
        print("Connection failed")


def on_message(client, userdata, message):
    # linux
    # db = TinyDB('/pythonscript/db.json')
    db = TinyDB('C:/Users/sitas/Desktop/Database_Maid/db.json')
    Q = Query()
    result = message.payload.decode("utf-8", "strict")
    result_db = db.all()
    result_json = json.loads(result)
    result_len = len(result_json)
    result_id = y["id"]
    result_status = y["status"]

    if (result_len != 2):
        db.insert(y)

    if (result_len == 2):
        if (result_status == "3"):
            db.update({'status': "3"}, Q.id == '%s' % result_id)
        elif (result_status == "2"):
            db.update({'status': "2"}, Q.id == '%s' % result_id)
        elif (result_status == "1"):
            db.update({'status': "1"}, Q.id == '%s' % result_id)


broker_address = "192.168.1.1"
port = 1883
user = "Maid"
password = "MaId@101"

client = mqttClient.Client()
client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port=port)
client.loop_start()

client.subscribe("/maid/", 0)

app = FlaskAPI(__name__)


@app.route("/order/<a>", methods=['GET'])
def order(a):
    if request.method == 'GET':
        # linux
        # db = TinyDB('/pythonscript/db.json')
        db = TinyDB('C:/Users/sitas/Desktop/Database_Maid/db.json')
        Q = Query()
        b = db.search(Q.id == '%s' % a)
        c = b[0]
        d = c['order']
        e = d[0]
        return jsonify(d)


@app.route("/", methods=['GET', 'PUT'])
def index():
    if request.method == 'GET':
        # linux
        # db = TinyDB('/pythonscript/db.json')
        db = TinyDB('C:/Users/sitas/Desktop/Database_Maid/db.json')
        a = db.all()
        return jsonify(a)

    elif request.method == 'PUT':
        return jsonify({"TEST": "PASS"})


@app.route("/del", methods=['GET'])
def delete():
    if request.method == 'GET':
        # linux
        # db = TinyDB('/pythonscript/db.json')
        db = TinyDB('C:/Users/sitas/Desktop/Database_Maid/db.json')
        db.purge()
        return jsonify({"Delete": "OK"})


@app.route("/up/<a>/<b>", methods=['GET'])
def upstatus(a, b):
    if request.method == 'GET':
        # linux
        # db = TinyDB('/pythonscript/db.json')
        db = TinyDB('C:/Users/sitas/Desktop/Database_Maid/db.json')
        Q = Query()
        db.update({'status': b}, Q.id == '%s' % a)
        z = db.all()
        return jsonify(z)


@app.route("/date/<a>", methods=['GET'])
def date(a):
    if request.method == 'GET':
        # linux
        # db = TinyDB('/pythonscript/db.json')
        db = TinyDB('C:/Users/sitas/Desktop/Database_Maid/db.json')
        Q = Query()
        b = db.search(Q.date == '%s' % a)
        return jsonify(b)


if __name__ == "__main__":
    app.debug = True
    # app.run(host='0.0.0.0', port=5010)
    app.run(host='localhost', port=5000)
