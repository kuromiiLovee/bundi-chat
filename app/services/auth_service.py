import uuid

from fastapi import HTTPException, status
from tortoise.exceptions import IntegrityError

from ..core import exceptions
from ..models import User
from ..schemas import CreateUser
from ..utils.auth import hash_password


class AuthService:
    """
    Service class for handling user authentication and account management.
    """

    async def get_user(self, username: str):
        """
        Asynchronously retrieves a user from the database by matching the provided email address.
        """

        return await User.filter(username=username).first()

    async def user_exists(self, username: str) -> bool:
        """
        Check if a user with the given email exists in the database.
        """
        return await User.filter(username=username).exists()

    async def create_user_account(self, user: CreateUser):
        """Creates a new user account."""

        user_data = user.model_dump()

        user_exists = await self.user_exists(user_data["username"])

        if user_exists:
            raise exceptions.UserAlreadyExistsException()

        hashed_password = hash_password(user.password)

        # replace "password" in user_data with the hashed password
        user_data["password"] = hashed_password

        try:
            # create user account
            new_user = await User.create(**user_data)
            return new_user

        except IntegrityError as e:
            # Check if the error is due to a unique constraint violation - user account already exists
            if "UNIQUE constraint failed" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken! Please choose a different one.",
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected database error occurred: {str(e)}",
            )

    async def update_user_profile(self, user: User, user_data: dict):
        """
        Asynchronously updates the profile information of a user with the provided data.
        """

        for key, value in user_data.items():
            setattr(user, key, value)

        await user.save()
        return user
