#!/usr/bin/env python

# WS server that sends messages at random intervals

import asyncio
import websockets
import datetime
import random
import json

MOCK_MODE = True

async def time(websocket, path):
    while True:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        data = {'timestamps': [now]}
        await websocket.send(json.dumps(data))
        await asyncio.sleep(random.random() * 3)

if MOCK_MODE == True:
    start_server = websockets.serve(time, '127.0.0.1', 5678)
else:
    raise NotImplemented("Only mock mode is implemented")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


"""
edu:

jsonify() function in flask returns a flask.Response() object.
ref: https://stackoverflow.com/questions/7907596/json-dumps-vs-flask-jsonify

"""
