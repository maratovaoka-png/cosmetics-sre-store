from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "product_requests_total",
    "Total number of requests to product service"
)

PRODUCT_VIEW_COUNT = Counter(
    "cosmetic_product_views_total",
    "Total number of cosmetic product views"
)

REQUEST_LATENCY = Histogram(
    "product_request_latency_seconds",
    "Product service request latency"
)

products = [
    {
        "id": 1,
        "name": "Hydrating Face Cream",
        "category": "Skincare",
        "brand": "GlowCare",
        "price": 25.99,
        "stock": 50
    },
    {
        "id": 2,
        "name": "Matte Lipstick",
        "category": "Makeup",
        "brand": "BeautyLux",
        "price": 14.99,
        "stock": 100
    },
    {
        "id": 3,
        "name": "Vitamin C Serum",
        "category": "Skincare",
        "brand": "DermaGlow",
        "price": 32.50,
        "stock": 40
    },
    {
        "id": 4,
        "name": "Waterproof Mascara",
        "category": "Makeup",
        "brand": "LashPro",
        "price": 18.75,
        "stock": 80
    },
    {
        "id": 5,
        "name": "Rose Body Lotion",
        "category": "Body Care",
        "brand": "SoftSkin",
        "price": 21.00,
        "stock": 60
    }
]


@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return jsonify({
        "service": "product-service",
        "project": "Online Cosmetics Store",
        "status": "running"
    })


@app.route("/products")
@REQUEST_LATENCY.time()
def get_products():
    REQUEST_COUNT.inc()
    PRODUCT_VIEW_COUNT.inc()

    return jsonify({
        "products": products
    })


@app.route("/products/<int:product_id>")
@REQUEST_LATENCY.time()
def get_product(product_id):
    REQUEST_COUNT.inc()
    PRODUCT_VIEW_COUNT.inc()

    for product in products:
        if product["id"] == product_id:
            return jsonify(product)

    return jsonify({
        "error": "Cosmetic product not found"
    }), 404


@app.route("/health")
def health():
    return jsonify({
        "service": "product-service",
        "status": "healthy"
    })


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)