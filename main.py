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
    print(f"✅ Cliente conectado. Total conexiones: {len(active_connections)}")

    try:
        while True:
            # Espera mensajes del cliente
            data = await websocket.receive_text()
            # print(f"↓{data}")

            result = Procesamiento.clasificacion(data, token)
            # Opcional: responder al cliente
            await websocket.send_text(json.dumps(result))

            # Opcional: broadcast a todos
            # await broadcast(f"Broadcast: {data}")

    except WebSocketDisconnect:
        # Se desconectó el cliente
        active_connections.remove(websocket)
        print(f"Cliente desconectado. Quedan: {len(active_connections)}")
    except Exception as e:
        print(f"Error con cliente: {e}")
        active_connections.remove(websocket)

# Opcional: función para enviar a todos
async def broadcast(message: str):
    # Enviar mensaje a todas las conexiones activas
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except Exception as e:
            print(f"Error al enviar a un cliente: {e}")
            disconnected.append(connection)

    # Limpiar conexiones caídas
    for conn in disconnected:
        if conn in active_connections:
            active_connections.remove(conn)

# Opcional: endpoint para ver cuántos están conectados
@app.get("/status")
async def status():
    return {"connected_clients": len(active_connections)}