from fastapi import HTTPException, status


class InvalidTokenException(HTTPException):
    """Exception is thrown when user provided an expired invalid token."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The token is invalid or has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )


class RevokedTokenException(HTTPException):
    """Exception is raised when a user has provided a revoked token."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )


class AccessTokenRequiredException(HTTPException):
    """
    Exception is raised when a user has provided a refresh token instead of
    an access token.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="An access token is required to access this resource",
            headers={"WWW-Authenticate": "Bearer"},
        )


class RefreshTokenRequiredException(HTTPException):
    """
    Exception is raised when a user has provided an access token instead
    of a refresh token.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A refresh token is required to access this resource",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidUserCredentialsException(HTTPException):
    """Exception is thrown when a user has provided invalid credentials."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UserAlreadyExistsException(HTTPException):
    """
    Exception is thrown when a user has provided an email that exists.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )


class UsernameAlreadyExistsException(HTTPException):
    """Exception is thrown when a user has provided a username that exists."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this username already exists.",
        )


class PermissionRequiredException(HTTPException):
    """
    Exception is thrown when a user does not have permission to peform
    the current action or access an endpoint or a resource.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )


class AccountNotVerifiedException(HTTPException):
    """
    Exception is thrown when a user tries to perform an action without
    verifying their account.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is not verified. Please verify your account to proceed.",
        )


class UserNotFoundException(HTTPException):
    """Exception is thrown when a user is not found."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )


class PasswordIsShortException(HTTPException):
    """Exception is raised when password and confirm password is short."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too short! It must be at least 8 characters long.",
        )


class PasswordsDontMatchException(HTTPException):
    """Exception is raised if the password and confirm password don't match."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match!",
        )


class InvalidPasswordException(HTTPException):
    """
    Exception is raised if the user provides an invalid password.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password provided!",
        )


class RoomDoesNotExistException(HTTPException):
    """
    This exception is raised if the room does not exist.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found!",
        )


class UserIsBlockedFromJoiningRoomException(HTTPException):
    """
    This exception is raised if a user is blocked from joining a
    chat room due to failed login attempts.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Room access blocked due to multiple failed login attempts!",
        )


class UserBannedFromRoomException(HTTPException):
    """
    This exception is raised if a user is banned from joining a chat room.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are banned and can't rejoin this room!",
        )


class JoinChatRoomFailedException(HTTPException):
    """
    This exception is raised when a user's attempts to join a room chat
    exceeds their failed attempts.
    """

    def __init__(self, failed_attempts: int):
        self.failed_attempts = failed_attempts
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Incorrect password! You have {self.failed_attempts} attempts left.",
        )


class CannotDeleteRoomException(HTTPException):
    """
    This exception is raised if a user who is not the host
    tries to delete the room.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the host can delete this room!",
        )


class UserNotInRoomException(HTTPException):
    """
    This exception is raised if a user who is not a member
    of the room tries to leave the room.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this room!",
        )
