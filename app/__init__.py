from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from app.core.ws_manager import WebsocketConnectionManager

app = FastAPI()

manager = WebsocketConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message("Sent!", websocket)
            await manager.broadcast(f"Client ID: #{client_id} says {data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client ID: #{client_id} has left.")
