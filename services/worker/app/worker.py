import json
import time
import logging
import redis
import psycopg2
import os

SERVICE_NAME = "worker-service"

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "votedb")
DB_USER = os.getenv("DB_USER", "voteuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "votepass")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(SERVICE_NAME)

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

db_conn = psycopg2.connect(
    host=DB_HOST,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
db_conn.autocommit = True
db_cursor = db_conn.cursor()

logger.info("Worker started. Waiting for votes...")

while True:
    try:
        _, message = redis_client.blpop("votes")
        vote = json.loads(message)

        logger.info("Processing vote: %s", vote)

        db_cursor.execute(
            "INSERT INTO votes (vote) VALUES (%s)",
            (vote["vote"],)
        )

        logger.info("Vote saved to database: %s", vote)

    except Exception as e:
        logger.error("Worker error: %s", e)
        time.sleep(2)
