import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Event
import uuid

client = TestClient(app)

def test_ingest_and_dau():
    db = SessionLocal()
    db.query(Event).delete()
    db.commit()

    test_date = "2025-11-03T12:00:00+03:00"
    events = [
        {
            "event_id": str(uuid.uuid4()),
            "occurred_at": test_date,
            "user_id": 1,
            "event_type": "login",
            "properties": {}
        },
        {
            "event_id": str(uuid.uuid4()),
            "occurred_at": test_date,
            "user_id": 2,
            "event_type": "view_item",
            "properties": {}
        }
    ]
    
    response = client.post("/events", json=events)
    assert response.status_code == 200
    assert response.json()["inserted"] == 2

    today = "2025-11-03"
    response = client.get(f"/stats/dau?from_date={today}&to_date={today}")
    assert response.status_code == 200
    dau = response.json()
    assert dau[today] == 2
