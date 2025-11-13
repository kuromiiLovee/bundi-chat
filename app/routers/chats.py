from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.core.dependencies import get_current_user
from app.core.ws_manager import WebsocketConnectionManager
from app.schemas import User
from app.services import ChatService

router = APIRouter()
manager = WebsocketConnectionManager()


async def get_chat_service() -> ChatService:
    return ChatService()


@router.websocket("/ws/{room_link}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_link: str,
    service: ChatService = Depends(get_chat_service),
    user: User = Depends(get_current_user),
):
    await manager.connect(room_link, websocket)

    # send chat history when joining a room
    messages = await service.get_recent_message(room_link)
    for message in reversed(messages):
        await websocket.send_text(message.content)

    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_message("Sent!", websocket)
            await service.save_message(room_link, user.id, data)
            await manager.broadcast(room_link, data)

    except WebSocketDisconnect:
        await manager.disconnect(room_link, websocket)
        await manager.broadcast(room_link, f"{user.username} left")
