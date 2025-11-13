from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, Field, StringConstraints

validated_mobile_num = Annotated[
    str, StringConstraints(min_length=10, max_length=15, pattern=r"^\+?[1-9]\d{1,14}$")
]


class BaseUser(BaseModel):
    username: str
    password: str = Field(min_length=8)

    class Config:
        from_attributes = True


class User(BaseUser):
    """
    This schema represent a user.
    """

    id: str
    password: str | None = Field(default=None, exclude=True)  # hide user's password


class CreateUser(BaseUser):
    """This is a schema to create a user account."""

    pass


class CreatedUserResponse(BaseUser):
    """Response data for a newly created user."""

    id: str
    # don't show password in response data
    password: str | None = Field(default=None, exclude=True)

    class Config:
        from_attributes = True


class UserResponse(BaseUser):
    id: str
    is_verified: bool
