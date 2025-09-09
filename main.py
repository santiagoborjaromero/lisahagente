from fastapi import FastAPI, WebSocket
from fastapi.websockets import WebSocketDisconnect
# import asyncio
from src.procesamiento import Procesamiento
from src.cmds import saveLog
from src.functions import decrypt, validate_token
import json

app = FastAPI(title="LiSAH Sentinel 1.0")

active_connections: list[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token:str):
    await websocket.accept()
    active_connections.append(websocket)
    print(f"Cliente conectado. Total conexiones: {len(active_connections)}")

    valida_token = validate_token(token)
    if valida_token["status"] == True:
        try:
            while True:
                data = await websocket.receive_text()
                result = await Procesamiento.clasificacion(data, token)
                await websocket.send_text(json.dumps(result))

        except WebSocketDisconnect:
            active_connections.remove(websocket)
            print(f"Cliente desconectado. Quedan: {len(active_connections)}")
        except Exception as err:
            print(f"Error: {err}")
            active_connections.remove(websocket)
    else:
        await websocket.send_text("TOKEN NO VALIDO")
        saveLog("NO VALIDO", "TOKEN")
    

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