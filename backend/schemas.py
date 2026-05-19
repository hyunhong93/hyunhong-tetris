from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    nickname: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    nickname: str


class GameRecordCreate(BaseModel):
    score: int
    level: int
    lines: int


class GameRecordOut(BaseModel):
    id: int
    score: int
    level: int
    lines: int
    played_at: datetime

    model_config = {"from_attributes": True}


class TopScore(BaseModel):
    nickname: str
    score: int
