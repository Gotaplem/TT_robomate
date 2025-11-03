from sqlalchemy import create_engine, Column, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- база данных SQLite в файле ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./events.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# --- модель события ---
class Event(Base):
    __tablename__ = "events"

    event_id = Column(String, primary_key=True, index=True)
    occurred_at = Column(DateTime, index=True)
    user_id = Column(String, index=True)
    event_type = Column(String, index=True)
    properties = Column(JSON)

# --- создать таблицы ---
def init_db():
    Base.metadata.create_all(bind=engine)
