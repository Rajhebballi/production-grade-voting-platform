import os
import logging
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

SERVICE_NAME = "result-service"

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "votedb")
DB_USER = os.getenv("DB_USER", "voteuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "votepass")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(SERVICE_NAME)

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/health", methods=["GET"])
def health():
    return jsonify(
        status="ok",
        service=SERVICE_NAME
    ), 200

@app.route("/results", methods=["GET"])
def results():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT vote, COUNT(*) 
        FROM votes
        GROUP BY vote
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    results = {vote: count for vote, count in rows}

    return jsonify(results), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
