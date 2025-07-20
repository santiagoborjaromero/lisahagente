import websockets
import asyncio
import configparser

PORT = 4700
connected = set()

async def echo(websocket):
    print("Un cliente se ha conectado")
    connected.add(websocket)
    try:
        async for message in websocket:
            print(f"Incomming: {message}")

            await websocket.send(f"Servidor responde a ti: {message}")

            # for conn in connected:
            #     if conn != websocket:
            #         await conn.send("Alguien dice" + message)
    except websockets.exceptions.ConnectionClosed as e:
        print("Un cliente se ha desconectado")
    finally:
        connected.remove(websocket)


async def main():
    async with websockets.serve(echo, "0.0.0.0", PORT):
        print(f"Escuchando {PORT}")
        await asyncio.Future()  # run forever

asyncio.run(main())
