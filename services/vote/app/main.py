import os
import json
import logging
import redis
from flask import Flask, request, jsonify

app = Flask(__name__)

SERVICE_NAME = "vote-service"
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(SERVICE_NAME)

@app.route("/health", methods=["GET"])
def health():
    try:
        redis_client.ping()
        redis_status = "ok"
    except Exception:
        redis_status = "down"

    return jsonify(
        status="ok",
        service=SERVICE_NAME,
        redis=redis_status
    ), 200

@app.route("/vote", methods=["POST"])
def vote():
    data = request.get_json()

    if not data or "vote" not in data:
        return jsonify(error="Missing 'vote' field"), 400

    payload = {"vote": data["vote"]}

    redis_client.rpush("votes", json.dumps(payload))
    logger.info("Vote queued: %s", payload)

    return jsonify(
        message="Vote accepted",
        vote=data["vote"]
    ), 202

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
