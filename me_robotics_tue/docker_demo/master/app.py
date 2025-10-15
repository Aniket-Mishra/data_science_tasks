import socket
import threading
import time

import requests
from flask import Flask, jsonify

app = Flask(__name__)
WORKER_URL = "http://worker:5010/status"


def check_worker():
    while True:
        try:
            r = requests.get(WORKER_URL, timeout=3)
            data = r.json()
            mood = data.get("status", "Unknown")
            print(f"[master] worker mood: {mood}", flush=True)
        except Exception as e:
            print(f"[master] error contacting worker: {e}")
        time.sleep(10)


@app.route("/ping")
def ping():
    return jsonify(
        status="ok",
        status_code=200,
        message="I am the master!",
        host=socket.gethostname(),
        time=time.time(),
    )


@app.route("/hello/<name>")
def hello(name):
    return jsonify(
        status="ok",
        status_code=200,
        message=f"Hello {name}!",
        from_service="master",
        host=socket.gethostname(),
    )


@app.route("/")
def root():
    return jsonify(service="master", endpoints=["/ping", "/hello/<name>"])


if __name__ == "__main__":
    threading.Thread(target=check_worker, daemon=True).start()
    app.run(host="0.0.0.0", port=5010)
