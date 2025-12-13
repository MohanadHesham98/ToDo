# todo-service/app/models.py
# ---------------------------------------------------------------------------
from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    done: bool = False
    alarm_time: Optional[datetime] = None
    user_id: Optional[int] = Field(default=None)
    user_email: Optional[str] = None
    alarm_sent: bool = Field(default=False)

