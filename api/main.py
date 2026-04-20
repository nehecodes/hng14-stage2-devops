from fastapi import FastAPI
from config import settings
import redis
import uuid


app = FastAPI()
host = settings.redis_host
port = settings.redis_port
redis_conn = redis.Redis(
    host=host,
    port=port,
    decode_responses=True,
)


@app.post("/jobs")
async def create_job():
    job_id = str(uuid.uuid4())
    try:
        redis_conn.lpush("job", job_id)
        redis_conn.hset(f"job:{job_id}", "status", "queued")
        return {"job_id": job_id}
    except Exception as e:
        return {"message": f"failed to queue job {job_id}: {e}"}


@app.get("/jobs/{job_id}")
async def get_job(job_id: str):
    try:
        status = redis_conn.hget(f"job:{job_id}", "status")
        if not status:
            return {"error": "not found"}
        return {"job_id": job_id, "status": status}
    except Exception as e:
        return {"message": f"some error occured: {e}"}
