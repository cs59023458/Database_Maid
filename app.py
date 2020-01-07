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
    x = message.payload.decode("utf-8", "strict")
    y = json.loads(x)
    # linux
    # db = TinyDB('/pythonscript/db.json')
    db = TinyDB('C:/Users/sitas/Desktop/Database_Maid/db.json')
    db.insert(y)


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

client.subscribe("/maid/")

app = FlaskAPI(__name__)


@app.route("/test", methods=['GET', 'PUT'])
def test():
    # read file data
    # reconsctuction data
    if request.method == 'GET':
        # linux
        # db = TinyDB('/pythonscript/db.json')
        db = TinyDB('C:/Users/sitas/Desktop/Database_Maid/db.json')
        a = db.all()
        return jsonify(a)

    elif request.method == 'PUT':
        return jsonify({"TEST": "PASS"})
    # return data


@app.route("/del", methods=['GET'])
def delete():
    if request.method == 'GET':
        # linux
        # db = TinyDB('/pythonscript/db.json')
        db = TinyDB('C:/Users/sitas/Desktop/Database_Maid/db.json')
        db.purge()
        return jsonify({"Delete": "OK"})


@app.route("/up/<a>", methods=['GET'])
def up(a):
    # read file data
    # reconsctuction data
    if request.method == 'GET':
        # linux
        # db = TinyDB('/pythonscript/db.json')
        db = TinyDB('C:/Users/sitas/Desktop/Database_Maid/db.json')
        Q = Query()
        db.update({'status': "0"}, Q.id == '%s' % a)
        # b = db.search(Q.id == '%s' % a)
        return jsonify({"id": a, "status": "2"})

if __name__ == "__main__":
    app.debug = True
    # app.run(host='0.0.0.0', port=5010)
    app.run(host='localhost', port=5000)
