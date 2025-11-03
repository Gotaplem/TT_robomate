from fastapi import APIRouter, Query
from typing import List
from app.database import SessionLocal, Event
from datetime import datetime, timedelta
from sqlalchemy import func, desc
import uuid

router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "pong"}

@router.post("/events")
def ingest_events(events: List[dict]):
    db = SessionLocal()
    inserted = 0
    for ev in events:
        if not ev.get("event_id"):
            ev["event_id"] = str(uuid.uuid4())
        exists = db.query(Event).filter_by(event_id=ev["event_id"]).first()
        if exists:
            continue
        e = Event(
            event_id=ev["event_id"],
            occurred_at=datetime.fromisoformat(ev["occurred_at"]),
            user_id=ev["user_id"],
            event_type=ev["event_type"],
            properties=ev.get("properties", {})
        )
        db.add(e)
        inserted += 1
    db.commit()
    return {"inserted": inserted}

# --- GET /stats/dau ---
@router.get("/stats/dau")
def get_dau(from_date: str = Query(...), to_date: str = Query(...)):
    db = SessionLocal()
    start = datetime.fromisoformat(from_date)
    end = datetime.fromisoformat(to_date)
    delta = timedelta(days=1)
    result = {}
    current = start
    while current <= end:
        next_day = current + delta
        count = db.query(Event.user_id).filter(
            Event.occurred_at >= current,
            Event.occurred_at < next_day
        ).distinct().count()
        result[current.strftime("%Y-%m-%d")] = count
        current = next_day
    return result

@router.get("/stats/top-events")
def top_events(from_date: str = Query(...), to_date: str = Query(...), limit: int = 10):
    db = SessionLocal()
    start = datetime.fromisoformat(from_date)
    end = datetime.fromisoformat(to_date)

    results = (
        db.query(Event.event_type, func.count(Event.event_type).label("count"))
        .filter(Event.occurred_at >= start, Event.occurred_at <= end)
        .group_by(Event.event_type)
        .order_by(desc("count"))
        .limit(limit)
        .all()
    )

    return [{"event_type": r[0], "count": r[1]} for r in results]

@router.get("/stats/retention")
def retention(start_date: str = Query(...), windows: int = Query(3)):
    db = SessionLocal()
    start = datetime.fromisoformat(start_date)
    result = {}

    cohort_users = db.query(Event.user_id).filter(
        Event.occurred_at >= start,
        Event.occurred_at < start + timedelta(days=1)
    ).distinct().all()
    cohort_users = [u[0] for u in cohort_users]

    for i in range(windows):
        day = start + timedelta(days=i)
        count = db.query(Event.user_id).filter(
            Event.user_id.in_(cohort_users),
            Event.occurred_at >= day,
            Event.occurred_at < day + timedelta(days=1)
        ).distinct().count()
        result[day.strftime("%Y-%m-%d")] = count

    return result
