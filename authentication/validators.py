from pydantic import BaseModel


class UserLogin(BaseModel):
    email: str
    first_name: str
    last_name: str
    access: str
    refresh: str


class UserTokens(BaseModel):
    token: str
    refresh: str
