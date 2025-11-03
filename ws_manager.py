from fastapi.websockets import WebSocket


class WebsocketConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()

        # append new user to active connections
        self.active_connections.append(ws)

    async def disconnect(self, ws: WebSocket):
        """
        Disconnect a user if they leave or a disconnected from the endpoint.
        """
        self.active_connections.remove(ws)

    async def send_message(self, msg: str, ws: WebSocket):
        await ws.send_text(msg)

    async def broadcast(self, msg: str):
        for connection in self.active_connections:
            print(f"Connection: {connection}")
            await connection.send_text(msg)
