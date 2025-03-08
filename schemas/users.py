from pydantic import BaseModel

# --------------------------
# User Creation Model
# --------------------------
class UserCreate(BaseModel):
    """
    Pydantic model for creating a new user.

    Attributes:
        username (str): The username of the user.
        password (str): The plain-text password for the user.
    """
    username: str
    password: str