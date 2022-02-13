from enum import Enum

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


class AuthProviders(str, Enum):
    google = "google"
    email = "email"

    @staticmethod
    def valid_providers():
        return (
            (getattr(AuthProviders, item.value), item.value) for item in AuthProviders
        )
