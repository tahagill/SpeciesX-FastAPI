from pydantic import BaseModel

class User(BaseModel):
    username: str
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str
