import socket
import time

from flask import Flast, jsonify

app = Flast(__name__)


@app.route("/ping")
def ping():
    return jsonify(
        status="ok",
        status_code=200,
        message="I am the master!",
        host=socket.gethostname(),
        time=time.time(),
    )


@app.route("/hellp/<name>")
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
    app.run(host="0.0.0.0", port=5000)
