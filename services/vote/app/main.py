import json
import logging
import os

import redis
from flask import Flask, request, jsonify

from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# -----------------------------
# Basic app setup
# -----------------------------

app = Flask(__name__)

SERVICE_NAME = "vote-service"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(SERVICE_NAME)

# -----------------------------
# Redis connection
# -----------------------------

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

# -----------------------------
# Prometheus metrics
# -----------------------------

# Count how many HTTP requests we receive
REQUEST_COUNT = Counter(
    "vote_service_requests_total",
    "Total number of HTTP requests received",
    ["method", "endpoint"]
)

# Count how many votes we receive (cats, dogs, etc.)
VOTES_COUNT = Counter(
    "votes_received_total",
    "Total number of votes received",
    ["option"]
)

# -----------------------------
# Routes
# -----------------------------

@app.route("/health", methods=["GET"])
def health():
    REQUEST_COUNT.labels(method="GET", endpoint="/health").inc()
    return jsonify(status="ok", service=SERVICE_NAME), 200


@app.route("/vote", methods=["POST"])
def vote():
    REQUEST_COUNT.labels(method="POST", endpoint="/vote").inc()

    data = request.get_json(force=True)
    vote_option = data.get("vote")

    if not vote_option:
        return jsonify(error="vote is required"), 400

    # Push vote to Redis queue
    redis_client.rpush("votes", json.dumps({"vote": vote_option}))

    # Count the vote
    VOTES_COUNT.labels(option=vote_option).inc()

    logger.info("Vote accepted: %s", vote_option)

    return jsonify(message="Vote accepted", vote=vote_option), 202


@app.route("/metrics", methods=["GET"])
def metrics():
    """
    Endpoint for Prometheus to scrape metrics
    """
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


# -----------------------------
# App start
# -----------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
