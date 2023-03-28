from pydantic import BaseModel


class Source(BaseModel):
    user_id: str
    name: str
    text: str


class LoginInput(BaseModel):
    username: str
    password: str


class QueryInput(BaseModel):
    query: str


class User(BaseModel):
    username: str
    email: str
    password: str
    user_type: str
