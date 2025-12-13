# todo-service/app/schemas.py
# ---------------------------------------------------------------------------
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    done: Optional[bool] = False
    alarm_time: Optional[datetime] = None
    user_email: Optional[str] = None

class TodoRead(TodoCreate):
    id: int
    user_email: Optional[str] = None

    class Config:
        orm_mode = True


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None
    alarm_time: Optional[datetime] = None
    alarm_sent: Optional[bool] = None
