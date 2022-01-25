#!/usr/bin/env python

# import asyncio
# import websockets

# async def hello():
#     uri = "ws://localhost:8765"
#     # websocket closed automatically when exiting the context (w/ connect)
#     # async for websocket in websockets.connect(uri): # infinite connection to serveur
#     async with websockets.connect(uri) as websocket:
#         name = input("What's your name? ")

#         await websocket.send(name)  # send name input to server on the same uri
#         print(f">>> {name}")

#         greeting = await websocket.recv()
#         print(f"<<< {greeting}")

#     # Use this pour avoir une loop infinie en se reco au serveur
#     # async for websocket in websockets.connect(...):
#     # try:
#     #     ...
#     # except websockets.ConnectionClosed:
#     #     continue

# if __name__ == "__main__":
#     asyncio.run(hello())


# Code pour le broadcast

import asyncio
import websockets
import json


async def hello():
    uri = "ws://localhost:8765"
    # websocket closed automatically when exiting the context (w/ connect)
    # async for websocket in websockets.connect(uri): # infinite connection to serveur
    async with websockets.connect(uri) as websocket:
        intro = await websocket.recv()
        print(f"<<< {intro}")

        value = input("plus or minus\t")
        name = json.dumps({"action": "{}".format(value)})
        await websocket.send(name)  # send name input to server on the same uri


        greeting = await websocket.recv()
        print(f"<<< {greeting}")

    # Use this pour avoir une loop infinie en se reco au serveur
    # async for websocket in websockets.connect(...):
    # try:
    #     ...
    # except websockets.ConnectionClosed:
    #     continue

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(hello())
    # asyncio.run(hello())



