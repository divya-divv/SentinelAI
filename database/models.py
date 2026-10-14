from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from database.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)

    timestamp = Column(String)
    service = Column(String)

    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    response_time_ms = Column(Float)
    error_rate = Column(Float)

    risk_score = Column(Integer)
    risk_level = Column(String)

    is_anomaly = Column(Boolean)
    anomaly_score = Column(Float)

    explanation = Column(Text)
    reasons = Column(Text)
    recommendations = Column(Text)