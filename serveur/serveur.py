#!/usr/bin/env python

# import asyncio
# import websockets

# async def hello(websocket):
#     name = await websocket.recv()   # recoit le nom du client
#     print(f"<<< {name}")

#     greeting = f"Hello {name}!"

#     await websocket.send(greeting)  # envoie un greeting au client
#     print(f">>> {greeting}")

#     broadcast_msg = "Hello to everyone on this server !"
#     await websockets.broadcast(websocket, broadcast_msg)

# async def main():
#     # Open server to listen on host localhost port 8765
#     async with websockets.serve(hello, "localhost", 8765):
#         await asyncio.Future()  # run forever

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print("Server stopped")


#!/usr/bin/env python

import asyncio
import json
import logging
import websockets

logging.basicConfig()

USERS = set()

VALUE = 0

def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})

def value_event():
    return json.dumps({"type": "value", "value": VALUE})

async def counter(websocket):
    # Envoie aux clients a sa connexion un msg sur combien il y a de users
    # connectes
    # Recoie des msg en json pour modifier la VALUE
    global USERS, VALUE
    try:
        # Register user
        USERS.add(websocket)
        websockets.broadcast(USERS, users_event())
        # Send current state to user
        await websocket.send(value_event())
        # Manage state changes
        async for message in websocket:
            event = json.loads(message)
            print(event)
            if event["action"] == "minus":
                VALUE -= 1
                websockets.broadcast(USERS, value_event())
            elif event["action"] == "plus":
                VALUE += 1
                websockets.broadcast(USERS, value_event())
            else:
                logging.error("unsupported event: %s", event)
    finally:
        # Unregister user
        USERS.remove(websocket)
        websockets.broadcast(USERS, users_event())

async def main():
    async with websockets.serve(counter, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())