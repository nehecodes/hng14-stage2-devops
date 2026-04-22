from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

mock_redis = MagicMock()

with patch("redis.Redis", return_value=mock_redis):
    from main import app

client = TestClient(app)


def setup_function():
    """Reset all mock call history before each test."""
    mock_redis.reset_mock()


#  Test 1: Health check


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"app": "ok"}


# Test 2: Create job


def test_create_job_queues_and_returns_job_id():
    response = client.post("/jobs")

    assert response.status_code == 200

    body = response.json()
    assert "job_id" in body

    job_id = body["job_id"]

    mock_redis.lpush.assert_called_once_with("job", job_id)

    mock_redis.hset.assert_called_once_with(f"job:{job_id}", "status", "queued")


def test_create_job_returns_error_message_when_redis_is_down():
    mock_redis.lpush.side_effect = Exception("Connection refused")

    response = client.post("/jobs")

    assert response.status_code == 200
    assert "failed to queue job" in response.json()["message"]

    mock_redis.lpush.side_effect = None


# Test 3: Get job


def test_get_job_returns_status_when_job_exists():
    mock_redis.hget.return_value = "queued"

    response = client.get("/jobs/some-job-id")

    assert response.status_code == 200
    assert response.json() == {"job_id": "some-job-id", "status": "queued"}
    mock_redis.hget.assert_called_once_with("job:some-job-id", "status")


def test_get_job_returns_not_found_when_job_missing():
    mock_redis.hget.return_value = None

    response = client.get("/jobs/nonexistent-id")

    assert response.status_code == 200
    assert response.json() == {"error": "not found"}


def test_get_job_returns_error_message_when_redis_is_down():
    mock_redis.hget.side_effect = Exception("Connection refused")

    response = client.get("/jobs/some-job-id")

    assert response.status_code == 200
    assert "some error occured" in response.json()["message"]

    mock_redis.hget.side_effect = None
