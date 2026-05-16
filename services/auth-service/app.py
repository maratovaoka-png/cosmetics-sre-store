from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest
import time

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "auth_requests_total",
    "Total number of requests to auth service"
)

LOGIN_COUNT = Counter(
    "auth_login_total",
    "Total number of login attempts"
)

REQUEST_LATENCY = Histogram(
    "auth_request_latency_seconds",
    "Auth service request latency"
)

users = {
    "aigerim": {
        "password": "12345",
        "email": "aigerim@example.com"
    }
}


@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return jsonify({
        "service": "auth-service",
        "project": "Online Cosmetics Store",
        "status": "running"
    })


@app.route("/register", methods=["POST"])
@REQUEST_LATENCY.time()
def register():
    REQUEST_COUNT.inc()

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not username or not password or not email:
        return jsonify({
            "error": "username, password and email are required"
        }), 400

    users[username] = {
        "password": password,
        "email": email
    }

    return jsonify({
        "message": "Cosmetics store user registered successfully",
        "username": username,
        "email": email
    })


@app.route("/login", methods=["POST"])
@REQUEST_LATENCY.time()
def login():
    REQUEST_COUNT.inc()
    LOGIN_COUNT.inc()

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if username in users and users[username]["password"] == password:
        return jsonify({
            "message": "Login successful",
            "username": username
        })

    return jsonify({
        "error": "Invalid username or password"
    }), 401


@app.route("/health")
def health():
    return jsonify({
        "service": "auth-service",
        "status": "healthy"
    })


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)