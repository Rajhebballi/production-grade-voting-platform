import logging
import os
import psycopg2

from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# -----------------------------
# App setup
# -----------------------------

app = Flask(__name__)
SERVICE_NAME = "result-service"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(SERVICE_NAME)

# -----------------------------
# Database config
# -----------------------------

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "votedb")
DB_USER = os.getenv("DB_USER", "voteuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "votepass")

# -----------------------------
# Prometheus metrics
# -----------------------------

REQUEST_COUNT = Counter(
    "result_service_requests_total",
    "Total number of HTTP requests received by result service",
    ["method", "endpoint"]
)

DB_QUERY_COUNT = Counter(
    "result_service_db_queries_total",
    "Total number of database queries executed by result service"
)

# -----------------------------
# Helpers
# -----------------------------

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# -----------------------------
# Routes
# -----------------------------

@app.route("/health", methods=["GET"])
def health():
    REQUEST_COUNT.labels(method="GET", endpoint="/health").inc()
    return jsonify(status="ok", service=SERVICE_NAME), 200


@app.route("/results", methods=["GET"])
def results():
    REQUEST_COUNT.labels(method="GET", endpoint="/results").inc()

    conn = get_db_connection()
    cur = conn.cursor()

    DB_QUERY_COUNT.inc()

    cur.execute("SELECT vote, COUNT(*) FROM votes GROUP BY vote;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    results = {vote: count for vote, count in rows}

    logger.info("Results fetched: %s", results)

    return jsonify(results), 200


@app.route("/metrics", methods=["GET"])
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


# -----------------------------
# App start
# -----------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
