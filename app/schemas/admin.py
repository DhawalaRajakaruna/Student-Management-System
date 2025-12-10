from pydantic import BaseModel


class AdminCreate(BaseModel):
    username: str
    password: str

class AdminUpdate(BaseModel):
    username: str | None = None
    password: str | None = None