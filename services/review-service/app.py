from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest
import uuid

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "review_requests_total",
    "Total number of requests to review service"
)

REVIEW_COUNT = Counter(
    "cosmetic_reviews_created_total",
    "Total number of cosmetic product reviews"
)

REQUEST_LATENCY = Histogram(
    "review_request_latency_seconds",
    "Review service request latency"
)

reviews = [
    {
        "review_id": "1",
        "product_id": 1,
        "username": "demo_user",
        "rating": 5,
        "comment": "Very good face cream"
    }
]


@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return jsonify({
        "service": "review-service",
        "project": "Online Cosmetics Store",
        "status": "running"
    })


@app.route("/reviews", methods=["GET"])
def get_reviews():
    REQUEST_COUNT.inc()
    return jsonify({
        "reviews": reviews
    })


@app.route("/reviews", methods=["POST"])
@REQUEST_LATENCY.time()
def create_review():
    REQUEST_COUNT.inc()

    data = request.get_json()

    product_id = data.get("product_id")
    username = data.get("username")
    rating = data.get("rating")
    comment = data.get("comment")

    if not product_id or not username or not rating or not comment:
        return jsonify({
            "error": "product_id, username, rating and comment are required"
        }), 400

    review = {
        "review_id": str(uuid.uuid4()),
        "product_id": product_id,
        "username": username,
        "rating": rating,
        "comment": comment
    }

    reviews.append(review)
    REVIEW_COUNT.inc()

    return jsonify({
        "message": "Cosmetic product review created successfully",
        "review": review
    })


@app.route("/health")
def health():
    return jsonify({
        "service": "review-service",
        "status": "healthy"
    })


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006)