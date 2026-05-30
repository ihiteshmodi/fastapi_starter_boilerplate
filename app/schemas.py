from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Principal(BaseModel):
    username: str
    scope: str


class HelloResponse(BaseModel):
    message: str
    username: str
    scope: str
