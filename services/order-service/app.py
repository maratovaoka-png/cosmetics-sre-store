from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest
import os
import uuid

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "order_requests_total",
    "Total number of requests to order service"
)

ORDER_COUNT = Counter(
    "cosmetic_orders_created_total",
    "Total number of cosmetic orders created"
)

ORDER_ERROR_COUNT = Counter(
    "cosmetic_order_errors_total",
    "Total number of cosmetic order errors"
)

REQUEST_LATENCY = Histogram(
    "order_request_latency_seconds",
    "Order service request latency"
)

orders = []


@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return jsonify({
        "service": "order-service",
        "project": "Online Cosmetics Store",
        "status": "running"
    })


@app.route("/orders", methods=["POST"])
@REQUEST_LATENCY.time()
def create_order():
    REQUEST_COUNT.inc()

    fail_mode = os.getenv("FAIL_MODE", "false")

    if fail_mode == "true":
        ORDER_ERROR_COUNT.inc()
        return jsonify({
            "error": "Order Service incident: database configuration error"
        }), 500

    data = request.get_json()

    username = data.get("username")
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if not username or not product_id or not quantity:
        ORDER_ERROR_COUNT.inc()
        return jsonify({
            "error": "username, product_id and quantity are required"
        }), 400

    order = {
        "order_id": str(uuid.uuid4()),
        "username": username,
        "product_id": product_id,
        "quantity": quantity,
        "status": "created"
    }

    orders.append(order)
    ORDER_COUNT.inc()

    return jsonify({
        "message": "Cosmetics order created successfully",
        "order": order
    })


@app.route("/orders")
def get_orders():
    REQUEST_COUNT.inc()
    return jsonify({
        "orders": orders
    })


@app.route("/health")
def health():
    return jsonify({
        "service": "order-service",
        "status": "healthy"
    })


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)