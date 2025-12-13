from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import SQLModel, Session, select
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

from .database import engine, get_session
from .models import Todo
from .schemas import TodoCreate, TodoRead, TodoUpdate

app = FastAPI(title="Todo Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
AUTH_URL = os.getenv("AUTH_URL", "http://auth-service:8001")


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        res = requests.get(
            f"{AUTH_URL}/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        if res.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")
        return res.json()
    except Exception:
        raise HTTPException(status_code=401, detail="Auth service not reachable")


@app.get("/todos", response_model=list[TodoRead])
def list_todos(current_user: dict = Depends(get_current_user)):
    with Session(engine) as session:
        stmt = select(Todo).where(Todo.user_id == current_user["id"])
        todos = session.exec(stmt).all()
    return todos


@app.post("/todos", response_model=TodoRead)
def create_todo(todo_in: TodoCreate, current_user: dict = Depends(get_current_user)):
    todo = Todo(
        **todo_in.dict(exclude={"user_email"}),
        user_id=current_user["id"],
        user_email=current_user["email"],
        alarm_sent=False
    )

    with Session(engine) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)

    return todo


@app.put("/todos/{todo_id}", response_model=TodoRead)
def update_todo(
    todo_id: int,
    todo_in: TodoUpdate,
    current_user: dict = Depends(get_current_user)
):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)

        if not todo or todo.user_id != current_user["id"]:
            raise HTTPException(status_code=404, detail="Todo not found")

        update_data = todo_in.dict(exclude_unset=True)

        if "alarm_time" in update_data:
            todo.alarm_sent = False

        for field, value in todo_in.dict(exclude_unset=True).items():
            setattr(todo, field, value)

        session.add(todo)
        session.commit()
        session.refresh(todo)

    return todo


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, current_user: dict = Depends(get_current_user)):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)

        if not todo or todo.user_id != current_user["id"]:
            raise HTTPException(status_code=404, detail="Todo not found")

        session.delete(todo)
        session.commit()

    return {"ok": True}


# ---------- INTERNAL (for alarm-service) ----------

@app.get("/internal/todos")
def internal_list_todos(db: Session = Depends(get_session)):
    todos = db.exec(select(Todo)).all()
    return [
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "done": t.done,
            "alarm_time": t.alarm_time,
            "user_id": t.user_id,
            "user_email": t.user_email,
            "alarm_sent": t.alarm_sent,
        }
        for t in todos
    ]


@app.put("/internal/todos/{todo_id}/alarm-sent")
def internal_mark_alarm_sent(todo_id: int, db: Session = Depends(get_session)):
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404)
    todo.alarm_sent = True
    db.add(todo)
    db.commit()
    return {"ok": True}
