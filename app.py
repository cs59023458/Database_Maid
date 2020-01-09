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
    x = message.payload.decode("utf-8", "strict")
    a = db.all()
    y = json.loads(x)
    if (y.id != a.id or a.id == None):
        # linux
        # db = TinyDB('/pythonscript/db.json')
        db.insert(y)

    if (len(y) == 2):
        # linux
        # db = TinyDB('/pythonscript/db.json')
        db = TinyDB('C:/Users/sitas/Desktop/Database_Maid/db.json')
        if (y.status == 0):
            Q = Query()
            db.update({'status': "0"}, Q.id == '%s' % a)
        elif (y.status == 1):
            Q = Query()
            db.update({'status': "1"}, Q.id == '%s' % a)
        elif (y.status == 2):
            Q = Query()
            db.update({'status': "2"}, Q.id == '%s' % a)


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

@app.route("/order/<a>", methods=['GET'])
def order(a):
    # read file data
    # reconsctuction data
    if request.method == 'GET':
        # linux
        # db = TinyDB('/pythonscript/db.json')
        db = TinyDB('C:/Users/sitas/Desktop/Database_Maid/db.json')
        Q = Query()
        b = db.search(Q.id == '%s' % a)
        c = b[0]
        d = c['order']
        # print(d)
        # print(type(d))
        e = d[0]
        # print(e['amount'])
        # print(type(e))
        return jsonify(d)
    # return data

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
