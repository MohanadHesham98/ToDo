import threading
import time
import requests
import os
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .email_sender import send_email

EGYPT_TZ = ZoneInfo("Africa/Cairo")

TODO_URL = os.getenv("TODO_URL", "http://todo-service:8002")

ALARM_CHECK_INTERVAL = int(os.getenv("ALARM_CHECK_INTERVAL", 60))
TODO_FETCH_RETRIES = int(os.getenv("TODO_FETCH_RETRIES", 5))
TODO_FETCH_DELAY = int(os.getenv("TODO_FETCH_DELAY", 5))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def fetch_todos():
    for attempt in range(1, TODO_FETCH_RETRIES + 1):
        try:
            res = requests.get(f"{TODO_URL}/internal/todos", timeout=5)
            if res.status_code == 200:
                return res.json()
            logging.warning(
                f"Attempt {attempt}: Failed to fetch todos: {res.status_code} {res.text}"
            )
        except Exception as e:
            logging.warning(f"Attempt {attempt}: Error fetching todos: {e}")

        time.sleep(TODO_FETCH_DELAY)

    logging.error("Failed to fetch todos after retries")
    return []


def mark_alarm_sent(todo_id: int):
    """
    Internal update to avoid auth issues
    """
    try:
        requests.put(
            f"{TODO_URL}/internal/todos/{todo_id}/alarm-sent",
            timeout=5
        )
    except Exception as e:
        logging.error(f"Failed to update alarm_sent for todo {todo_id}: {e}")


def check_todos():
    todos = fetch_todos()
    now = datetime.now(EGYPT_TZ)
    logging.info(f"Current time (Egypt): {now.isoformat()}")

    for t in todos:
        alarm_str = t.get("alarm_time")

        if not alarm_str or t.get("done") or t.get("alarm_sent"):
            continue

        try:
            alarm_dt = datetime.fromisoformat(alarm_str)

            if alarm_dt.tzinfo is None:
                alarm_dt = alarm_dt.replace(tzinfo=EGYPT_TZ)
            else:
                alarm_dt = alarm_dt.astimezone(EGYPT_TZ)

            diff_seconds = (now - alarm_dt).total_seconds()

            logging.info(
                f"Todo '{t['title']}': alarm_time={alarm_dt.isoformat()}, diff={diff_seconds} sec"
            )

            # window آمن للإرسال مرة واحدة
            if 0 <= diff_seconds <= ALARM_CHECK_INTERVAL:
                logging.info(
                    f"Alarm: Sending email to {t['user_email']} for todo '{t['title']}'"
                )

                send_email(
                    to_email=t["user_email"],
                    subject=f"Todo Alarm: {t['title']}",
                    body=(
                        f"Your todo '{t['title']}' is scheduled now.\n"
                        f"Description: {t.get('description', '')}"
                    )
                )

                mark_alarm_sent(t["id"])

        except Exception as e:
            logging.error(
                f"Failed processing alarm for todo '{t.get('title')}': {e}"
            )


def alarm_worker():
    logging.info("Alarm worker started")
    while True:
        try:
            check_todos()
        except Exception as e:
            logging.error(f"Error checking alarms: {e}")

        time.sleep(ALARM_CHECK_INTERVAL)


@app.on_event("startup")
def start_worker():
    threading.Thread(target=alarm_worker, daemon=True).start()


@app.get("/")
def root():
    return {"message": "Alarm service running"}
