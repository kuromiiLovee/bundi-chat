from tortoise import fields

from .base import BaseModel, TimestampMixin


class Chat(TimestampMixin, BaseModel):
    sender = fields.ForeignKeyField(
        "models.User",
        on_delete=fields.CASCADE,
        related_name="sender",
        null=False,
    )
    room = fields.ForeignKeyField(
        "models.Room",
        on_delete=fields.CASCADE,
        related_name="room_chats",
        null=False,
    )
    message = fields.TextField()

    class Meta:
        ordering = ["sender", "room"]
