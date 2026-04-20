import redis
import time
import os
import signal
import sys
from dotenv import load_dotenv

load_dotenv()

redis_conn = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    decode_responses=True,
)

shutdown = False


def handle_signal(sig, frame):
    global shutdown
    print("Shutting down gracefully...")
    shutdown = True


signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)


def process_job(job_id):
    try:
        redis_conn.hset(f"job: {job_id}", "status", "processing...")
        print(f"Processing job {job_id}")
        time.sleep(2)  # simulate work
        redis_conn.hset(f"job:{job_id}", "status", "completed")
        print(f"Done: {job_id}")
    except Exception as e:
        print(f"Error processing {job_id}: {e}")
        redis_conn.hset(f"job: {job_id}", "status", "failed")


while not shutdown:
    job = redis_conn.brpop("job", timeout=5)
    if job:
        job_id = job[1]
        process_job(job_id)
print("Worker stopped")
sys.exit(0)
