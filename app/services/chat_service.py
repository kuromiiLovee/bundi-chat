from app.models import Chat, Room


class ChatService:
    async def get_room(self, link: str):
        return await Room.filter(link=link)

    async def save_message(self, link: str, user_id: int, msg: str):
        room_id = self.get_room(link)
        return await Chat.create(room=room_id, sender=user_id, message=msg)

    async def get_recent_message(self, link: str, limit: int = 20):
        room_id = self.get_room(link=link)
        return await Chat.filter(room=room_id).order_by("-created_at").limit(limit)
