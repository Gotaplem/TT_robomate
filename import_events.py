import csv
import json
import sys
from datetime import datetime
from app.database import SessionLocal, Event

def import_csv(path):
    db = SessionLocal()
    inserted = 0
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # проверяем idempotency
            exists = db.query(Event).filter_by(event_id=row["event_id"]).first()
            if exists:
                continue

            # создаём объект Event
            e = Event(
                event_id=row["event_id"],
                occurred_at=datetime.fromisoformat(row["occurred_at"]),
                user_id=row["user_id"],
                event_type=row["event_type"],
                properties=json.loads(row["properties_json"]) if row["properties_json"] else {}
            )
            db.add(e)
            inserted += 1
    db.commit()
    print(f"Inserted {inserted} events")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python import_events.py <path-to-csv>")
        sys.exit(1)
    import_csv(sys.argv[1])
