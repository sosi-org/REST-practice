#!/usr/bin/env python

# WS server that sends messages at random intervals

import asyncio
import websockets
import datetime
import random
import json

MOCK_MODE = True

def generate_invoice():
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    random_money = float(int(random.random() * 15.0 *100))/100.0
    data = {'timestamps': [now], 'username': "sosi", 'amount': random_money}
    return data

async def connection_started(websocket, path):
    # conversation started
    print('someone connected? starting a new loop')
    while True:
        # 'infinite loop iteration: Keeps engaged by clinging to this client: sending from here to it (despite that one starting the conection)')
        print('iteration: sending data (as request) to the client that connected to me')

        mockdata = generate_invoice() # generate_message_item
        resp = await websocket.send(json.dumps(mockdata))
        print('responded back:', resp)
        await asyncio.sleep(random.random() * 3 * 0.3)

if MOCK_MODE == True:
    start_server = websockets.serve(connection_started, '127.0.0.1', 5678)
else:
    raise NotImplemented("Only mock mode is implemented")

print("Websocket server: going to starting the start_server")
# no waiting here
asyncio.get_event_loop().run_until_complete(start_server)
print("Websocket server started to serve")

print("Websocket server: run forever the event loop:")
# no waiting here. Keeps being in the listening state until the first one connects to it
asyncio.get_event_loop().run_forever()
print("Websocket server: exiting")

"""
edu:

jsonify() function in flask returns a flask.Response() object.
ref: https://stackoverflow.com/questions/7907596/json-dumps-vs-flask-jsonify

"""
