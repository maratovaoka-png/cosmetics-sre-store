from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest

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


@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return jsonify({
        "service": "notification-service",
        "project": "Online Cosmetics Store",
        "status": "running"
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

    NOTIFICATION_COUNT.inc()

    return jsonify({
        "message": "Notification sent successfully",
        "to": username,
        "notification": message
    })


@app.route("/health")
def health():
    return jsonify({
        "service": "notification-service",
        "status": "healthy"
    })


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)