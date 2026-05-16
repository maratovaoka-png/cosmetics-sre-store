from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest
import uuid

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "payment_requests_total",
    "Total number of requests to payment service"
)

PAYMENT_COUNT = Counter(
    "cosmetic_payments_total",
    "Total number of cosmetic store payments"
)

PAYMENT_ERROR_COUNT = Counter(
    "cosmetic_payment_errors_total",
    "Total number of payment errors"
)

REQUEST_LATENCY = Histogram(
    "payment_request_latency_seconds",
    "Payment service request latency"
)


@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return jsonify({
        "service": "payment-service",
        "project": "Online Cosmetics Store",
        "status": "running"
    })


@app.route("/payments", methods=["POST"])
@REQUEST_LATENCY.time()
def create_payment():
    REQUEST_COUNT.inc()

    data = request.get_json()

    order_id = data.get("order_id")
    amount = data.get("amount")
    payment_method = data.get("payment_method", "card")

    if not order_id or not amount:
        PAYMENT_ERROR_COUNT.inc()
        return jsonify({
            "error": "order_id and amount are required"
        }), 400

    payment = {
        "payment_id": str(uuid.uuid4()),
        "order_id": order_id,
        "amount": amount,
        "payment_method": payment_method,
        "status": "paid"
    }

    PAYMENT_COUNT.inc()

    return jsonify({
        "message": "Cosmetics order payment processed successfully",
        "payment": payment
    })


@app.route("/health")
def health():
    return jsonify({
        "service": "payment-service",
        "status": "healthy"
    })


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)