import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_idempotent_post_events():
    event_id = str(uuid.uuid4())
    event = [{
        "event_id": event_id,
        "occurred_at": "2025-11-03T12:00:00+03:00",
        "user_id": 1,
        "event_type": "login",
        "properties": {"device": "pc"}
    }]
    
    response1 = client.post("/events", json=event)
    assert response1.status_code == 200
    assert response1.json()["inserted"] == 1
    
    response2 = client.post("/events", json=event)
    assert response2.status_code == 200
    # не должно добавляться второй раз
    assert response2.json()["inserted"] == 0
