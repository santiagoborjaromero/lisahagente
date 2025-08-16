from fastapi import FastAPI, WebSocket
from fastapi.websockets import WebSocketDisconnect
import asyncio
from src.procesamiento import Procesamiento
import json

app = FastAPI()

active_connections: list[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token:str):
    await websocket.accept()
    active_connections.append(websocket)
    print(f"Cliente conectado. Total conexiones: {len(active_connections)}")

    try:
        while True:
            data = await websocket.receive_text()
            result = Procesamiento.clasificacion(data, token)
            await websocket.send_text(json.dumps(result))

    except WebSocketDisconnect:
        # Se desconectó el cliente
        active_connections.remove(websocket)
        print(f"Cliente desconectado. Quedan: {len(active_connections)}")
    except Exception as e:
        print(f"Error con cliente: {e}")
        active_connections.remove(websocket)

async def broadcast(message: str):
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except Exception as e:
            print(f"Error al enviar a un cliente: {e}")
            disconnected.append(connection)

    for conn in disconnected:
        if conn in active_connections:
            active_connections.remove(conn)

@app.get("/status")
async def status():
    return {"connected_clients": len(active_connections)}