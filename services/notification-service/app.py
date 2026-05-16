from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest
import redis
import os
import json

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "notification_requests_total",
    "Total number of requests to notification service"
)

NOTIFICATION_COUNT = Counter(
    "cosmetic_notifications_sent_total",
    "Total number of notifications sent"
)

REQUEST_LATENCY = Histogram(
    "notification_request_latency_seconds",
    "Notification service request latency"
)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return jsonify({
        "service": "notification-service",
        "project": "Online Cosmetics Store",
        "status": "running",
        "message_broker": "Redis"
    })


@app.route("/notifications", methods=["POST"])
@REQUEST_LATENCY.time()
def send_notification():
    REQUEST_COUNT.inc()

    data = request.get_json()

    username = data.get("username")
    message = data.get("message")

    if not username or not message:
        return jsonify({
            "error": "username and message are required"
        }), 400

    notification = {
        "username": username,
        "message": message
    }

    redis_client.rpush("cosmetics_notifications", json.dumps(notification))

    NOTIFICATION_COUNT.inc()

    return jsonify({
        "message": "Notification sent successfully and stored in Redis",
        "to": username,
        "notification": message
    })


@app.route("/notifications/queue", methods=["GET"])
def get_notification_queue():
    REQUEST_COUNT.inc()

    messages = redis_client.lrange("cosmetics_notifications", 0, -1)

    return jsonify({
        "message_broker": "Redis",
        "queue": [json.loads(item) for item in messages]
    })


@app.route("/health")
def health():
    return jsonify({
        "service": "notification-service",
        "status": "healthy",
        "message_broker": "Redis"
    })


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)