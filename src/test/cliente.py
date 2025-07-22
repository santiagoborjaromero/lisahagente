import websockets
import asyncio

async def listen():
    url = "ws://localhost:4700"

    async with websockets.connect(url) as ws:
        await ws.send("MIo")
        while True:
            msg = await ws.recv()
            print(msg)

asyncio.get_event_loop().run_until_complete(listen())