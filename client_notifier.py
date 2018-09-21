"""
    Uses WebSockets to notify the webapp client.
    interface:
        notify_newdata_arrival(new_invoice_event)
"""

"""edu:
    * for websockets see: https://websockets.readthedocs.io/en/stable/intro.html
"""

import asyncio
import websockets

def notify_newdata_arrival(new_invoice_event):
    pass


qq = with websockets.connect('ws://localhost:8765') as websocket:

"""
import asyncio
import websockets

async def hello():
    async with websockets.connect(
            'ws://localhost:8765') as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
"""
