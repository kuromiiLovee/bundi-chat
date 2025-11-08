from typing import Any, List

from fastapi import Depends, HTTPException

from ..core.exceptions import RevokedTokenException
from ..core.token_bearer import AccessTokenBearer
from ..models.user import User
from ..services import AuthService
from ..utils.auth import token_in_blacklist

auth_service = AuthService()


async def get_current_user(
    token: dict = Depends(AccessTokenBearer()),
):
    """
    Retrieve the current authenticated user based on the provided access token.

    Args:
        token (dict): A dictionary containing user information extracted from the access token.
        session (AsyncSession): The asynchronous database session dependency.

    Returns:
        User: The user object corresponding to the email found in the token.

    Raises:
        HTTPException: If the user cannot be found or the token is invalid.
    """
    jti = token.get("jti")

    # check if the access token is blacklisted
    if jti and await token_in_blacklist(jti):
        raise RevokedTokenException()

    get_username = token["user"]["username"]
    user = await auth_service.get_user(get_username)
    return user


class RoleChecker:
    """
    Dependency class for FastAPI route protection using Role Based Access Control (RBAC).
    This class can be used as a dependency in FastAPI endpoints to restrict access to users
    with specific roles and to ensure that the user is verified.

    Args:
        allowed_roles (List[str]): A list of roles that are allowed to access the endpoint.

    Methods:
        __call__(current_user: User = Depends(get_current_user)) -> Any:
            Checks if the current user is verified and has one of the allowed roles.
            Raises HTTPException with status code 403 if the user is not verified or does not have the required role.
    """

    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    async def __call__(self, current_user: User = Depends(get_current_user)) -> Any:

        if current_user.role in self.allowed_roles:
            return True

        raise HTTPException(
            status_code=403,
            detail="You don't have permission to access this resource!",
        )
