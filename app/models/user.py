from tortoise import fields

from .base import BaseModel, TimestampMixin


class User(TimestampMixin, BaseModel):
    username = fields.CharField(max_length=50, unique=True, index=True)
    password = fields.CharField(max_length=128)
    is_active = fields.BooleanField(default=True)

    class Meta:
        ordering = ["username"]
        table = "users"
