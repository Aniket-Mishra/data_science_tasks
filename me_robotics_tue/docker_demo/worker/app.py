import os
import random
import threading
import time

import requests
from flask import Flask, jsonify

app = Flask(__name__)

MASTER_HOST = os.getenv("MASTER_HOST", "master")
MASTER_PORT = os.getenv("MASTER_PORT", "5010")
NAME = os.getenv("HELLO_NAME", os.getenv("NAME", "Aniket Mishra"))
PING_INTERVAL = float(os.getenv("PING_INTERVAL", "1.0"))
HELLO_INTERVAL = float(os.getenv("HELLO_INTERVAL", "5.0"))


@app.route("/status")
def status():
    return jsonify(
        status=random.choice(
            ["Good", "Bad", "Stressed", "Happy", "Calm", "Resting"]
        )
    )


def url(path: str) -> str:
    return f"http://{MASTER_HOST}:{MASTER_PORT}/{path.lstrip('/')}"


def worker_loop():
    print(f"[worker] starting. master={MASTER_HOST}:{MASTER_PORT}")
    last_ping = 0.0
    last_hello = 0.0
    while True:
        now = time.time()
        if now - last_ping >= PING_INTERVAL:
            try:
                r = requests.get(url("ping"), timeout=2)
                print(f"[worker] ping -> {r.status_code}: {r.json()}")
            except Exception as e:
                print(f"[worker] ping error: {e}")
            last_ping = now
        if now - last_hello >= HELLO_INTERVAL:
            try:
                r = requests.get(url(f"hello/{NAME}"), timeout=3)
                print(f"[worker] hello -> {r.status_code}: {r.json()}")
            except Exception as e:
                print(f"[worker] hello error: {e}")
            last_hello = now
        time.sleep(0.2)


if __name__ == "__main__":
    threading.Thread(target=worker_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=5010)
