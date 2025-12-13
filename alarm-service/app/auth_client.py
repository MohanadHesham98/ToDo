import os
import time
import requests

AUTH_URL = os.getenv("AUTH_URL")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")  # token from a logged in user

def get_users_from_auth():
    url = f"{AUTH_URL}/me"
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    for i in range(10):
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                print("Auth returned:", response.status_code)
        except requests.exceptions.RequestException:
            print(f"Attempt {i+1} failed, retrying...")
            time.sleep(3)
    raise Exception("Failed to connect to auth-service")
