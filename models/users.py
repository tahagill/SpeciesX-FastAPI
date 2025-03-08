from pydantic import BaseModel
from typing import Optional

# --------------------------
# Base User Model
# --------------------------
class UserBase(BaseModel):
    """
    Base model for user data.

    Attributes:
        username (str): The username of the user.
        full_name (str | None): The full name of the user (optional).
        disabled (bool | None): Whether the user is disabled (optional).
    """
    username: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

# --------------------------
# User Creation Model
# --------------------------
class UserCreate(UserBase):
    """
    Model for creating a new user.

    Attributes:
        password (str): The plain-text password for the user.
    """
    password: str

# --------------------------
# User in Database Model
# --------------------------
class UserInDB(UserBase):
    """
    Model for user data stored in the database.

    Attributes:
        hashed_password (str): The hashed password for the user.
    """
    hashed_password: str

# --------------------------
# User Response Model
# --------------------------
class User(UserBase):
    """
    Model for user data returned in API responses.
    """
    pass