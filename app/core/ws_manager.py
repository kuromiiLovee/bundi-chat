from fastapi.websockets import WebSocket


class WebsocketConnectionManager:
    def __init__(self) -> None:
        self.rooms: dict[str, list[WebSocket]] = {}

    async def connect(self, room_link: str, ws: WebSocket):
        await ws.accept()

        # append new user to active connections
        self.rooms.setdefault(room_link, []).append(ws)

    async def disconnect(self, room_link: str, ws: WebSocket):
        """
        Disconnect a user if they leave or a disconnected from the endpoint.
        """
        if room_link in self.rooms:
            self.rooms[room_link].remove(ws)
            if not self.rooms[room_link]:
                del self.rooms[room_link]

    async def send_message(self, msg: str, ws: WebSocket):
        await ws.send_text(msg)

    async def broadcast(self, room_link: str, msg: str):
        for connection in self.rooms.get(room_link, []):
            await connection.send_text(msg)
