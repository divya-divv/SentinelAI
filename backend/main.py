from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
import json

from ai.risk_engine import calculate_risk
from ai.anomaly_detector import AnomalyDetector
from ai.explanation_engine import explain_event
from ai.recommendation_engine import generate_recommendations

from database.database import SessionLocal
from database.models import Event


# --------------------------------------------------
# SENTINELAI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="SentinelAI",
    description="Real-Time AI Operations Platform",
    version="2.1.0"
)


# --------------------------------------------------
# CORS CONFIGURATION
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# EVENT DATA MODEL
# --------------------------------------------------

class OperationalEvent(BaseModel):
    timestamp: str
    service: str
    cpu_usage: float
    memory_usage: float
    response_time_ms: float
    error_rate: float


# --------------------------------------------------
# APPLICATION STATE
# --------------------------------------------------

events: List[dict] = []

anomaly_detector = AnomalyDetector()


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# --------------------------------------------------
# TRAIN AI USING HISTORICAL DATABASE EVENTS
# --------------------------------------------------

def train_anomaly_detector_from_database(db: Session):
    """
    Load historical operational events from SQLite
    and train the anomaly detection model.
    """

    historical_events = (
        db.query(Event)
        .order_by(Event.id.asc())
        .all()
    )

    training_data = [
        {
            "cpu_usage": event.cpu_usage,
            "memory_usage": event.memory_usage,
            "response_time_ms": event.response_time_ms,
            "error_rate": event.error_rate
        }
        for event in historical_events
    ]

    if len(training_data) >= 10:
        return anomaly_detector.train(training_data)

    print(
        "AI MODEL: Waiting for at least 10 historical events. "
        f"Available: {len(training_data)}"
    )

    return False


# --------------------------------------------------
# HOME ROUTE
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "SentinelAI Backend is Running!",
        "status": "online"
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# --------------------------------------------------
# RECEIVE AND ANALYZE OPERATIONAL EVENTS
# --------------------------------------------------

@app.post("/events")
def receive_event(
    event: OperationalEvent,
    db: Session = Depends(get_db)
):
    event_data = event.model_dump()

    # 1. Calculate operational risk
    risk_result = calculate_risk(event_data)

    analyzed_event = {
        **event_data,
        "risk_score": risk_result["risk_score"],
        "risk_level": risk_result["risk_level"]
    }

    # 2. Train using historical SQLite data
    train_anomaly_detector_from_database(db)

    # 3. Detect operational anomalies
    anomaly_result = anomaly_detector.predict(event_data)

    analyzed_event.update({
        "is_anomaly": anomaly_result["is_anomaly"],
        "anomaly_score": anomaly_result["anomaly_score"],
        "ai_anomaly": anomaly_result["ai_anomaly"],
        "extreme_condition": anomaly_result["extreme_condition"],
        "detection_method": anomaly_result["detection_method"],
        "model_trained": anomaly_result["model_trained"]
    })

    # 4. Generate human-readable explanation
    explanation = explain_event(analyzed_event)

    analyzed_event.update({
        "explanation": explanation["summary"],
        "reasons": explanation["reasons"]
    })

    # 5. Generate recommendations
    recommendations = generate_recommendations(
        analyzed_event
    )

    analyzed_event["recommendations"] = recommendations

    # 6. Store event in application memory
    events.append(analyzed_event)

    # 7. Store event permanently in SQLite
    database_event = Event(
        timestamp=analyzed_event["timestamp"],
        service=analyzed_event["service"],
        cpu_usage=analyzed_event["cpu_usage"],
        memory_usage=analyzed_event["memory_usage"],
        response_time_ms=analyzed_event["response_time_ms"],
        error_rate=analyzed_event["error_rate"],
        risk_score=analyzed_event["risk_score"],
        risk_level=analyzed_event["risk_level"],
        is_anomaly=analyzed_event["is_anomaly"],
        anomaly_score=analyzed_event["anomaly_score"],
        explanation=analyzed_event["explanation"],
        reasons=json.dumps(analyzed_event["reasons"]),
        recommendations=json.dumps(
            analyzed_event["recommendations"]
        )
    )

    db.add(database_event)
    db.commit()
    db.refresh(database_event)

    analyzed_event["id"] = database_event.id

    return {
        "message": "Event analyzed and stored successfully",
        "event": analyzed_event
    }


# --------------------------------------------------
# GET ALL EVENTS
# --------------------------------------------------

@app.get("/events")
def get_events(
    db: Session = Depends(get_db)
):
    database_events = (
        db.query(Event)
        .order_by(Event.id.desc())
        .all()
    )

    result = []

    for event in database_events:
        result.append({
            "id": event.id,
            "timestamp": event.timestamp,
            "service": event.service,
            "cpu_usage": event.cpu_usage,
            "memory_usage": event.memory_usage,
            "response_time_ms": event.response_time_ms,
            "error_rate": event.error_rate,
            "risk_score": event.risk_score,
            "risk_level": event.risk_level,
            "is_anomaly": event.is_anomaly,
            "anomaly_score": event.anomaly_score,
            "explanation": event.explanation,
            "reasons": json.loads(
                event.reasons or "[]"
            ),
            "recommendations": json.loads(
                event.recommendations or "[]"
            )
        })

    return {
        "total_events": len(result),
        "events": result
    }


# --------------------------------------------------
# DASHBOARD STATISTICS
# --------------------------------------------------

@app.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db)
):
    database_events = db.query(Event).all()

    normal_count = 0
    warning_count = 0
    critical_count = 0
    anomaly_count = 0

    for event in database_events:

        if event.risk_level == "NORMAL":
            normal_count += 1

        elif event.risk_level == "WARNING":
            warning_count += 1

        elif event.risk_level == "CRITICAL":
            critical_count += 1

        if event.is_anomaly:
            anomaly_count += 1

    return {
        "total_events": len(database_events),
        "normal_events": normal_count,
        "warning_events": warning_count,
        "critical_events": critical_count,
        "anomalies": anomaly_count
    }