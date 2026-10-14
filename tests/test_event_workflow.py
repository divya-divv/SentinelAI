import unittest
from fastapi.testclient import TestClient

from backend.main import app
from database.database import SessionLocal
from database.models import Event


class TestEventWorkflow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_event_processing_workflow(self):
        event_data = {
            "timestamp": "2026-01-01T12:00:00Z",
            "service": "integration-test-service",
            "cpu_usage": 20,
            "memory_usage": 30,
            "response_time_ms": 100,
            "error_rate": 1
        }

        response = self.client.post(
            "/events",
            json=event_data
        )

        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        self.assertEqual(
            response_data["message"],
            "Event analyzed and stored successfully"
        )

        analyzed_event = response_data["event"]

        self.assertEqual(
            analyzed_event["service"],
            "integration-test-service"
        )

        self.assertIn("risk_score", analyzed_event)
        self.assertIn("risk_level", analyzed_event)
        self.assertIn("is_anomaly", analyzed_event)
        self.assertIn("explanation", analyzed_event)
        self.assertIn("recommendations", analyzed_event)
        self.assertIn("id", analyzed_event)

        self.assertIsInstance(
            analyzed_event["recommendations"],
            list
        )

        db = SessionLocal()

        try:
            saved_event = (
                db.query(Event)
                .filter(
                    Event.id == analyzed_event["id"]
                )
                .first()
            )

            self.assertIsNotNone(saved_event)

            self.assertEqual(
                saved_event.service,
                "integration-test-service"
            )

        finally:
            if saved_event is not None:
                db.delete(saved_event)
                db.commit()

            db.close()


if __name__ == "__main__":
    unittest.main()
