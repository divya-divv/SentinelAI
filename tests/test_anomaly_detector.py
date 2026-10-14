import unittest
from ai.anomaly_detector import AnomalyDetector


class TestAnomalyDetector(unittest.TestCase):

    def setUp(self):
        self.detector = AnomalyDetector()

    def make_event(
        self,
        cpu=20,
        memory=30,
        response_time=100,
        error_rate=1
    ):
        return {
            "cpu_usage": cpu,
            "memory_usage": memory,
            "response_time_ms": response_time,
            "error_rate": error_rate
        }

    def test_training_requires_at_least_10_events(self):
        events = [
            self.make_event()
            for _ in range(9)
        ]

        result = self.detector.train(events)

        self.assertFalse(result)
        self.assertFalse(self.detector.is_trained)

    def test_model_trains_with_10_events(self):
        events = [
            self.make_event(
                cpu=20 + i,
                memory=30 + i,
                response_time=100 + i * 5,
                error_rate=1
            )
            for i in range(10)
        ]

        result = self.detector.train(events)

        self.assertTrue(result)
        self.assertTrue(self.detector.is_trained)

    def test_prediction_before_training(self):
        event = self.make_event()

        result = self.detector.predict(event)

        self.assertFalse(result["model_trained"])
        self.assertFalse(result["ai_anomaly"])
        self.assertFalse(result["is_anomaly"])
        self.assertEqual(result["detection_method"], "NONE")

    def test_extreme_conditions_are_detected(self):
        event = self.make_event(
            cpu=98,
            memory=40,
            response_time=100,
            error_rate=1
        )

        result = self.detector.predict(event)

        self.assertTrue(result["extreme_condition"])
        self.assertTrue(result["is_anomaly"])
        self.assertEqual(
            result["detection_method"],
            "CRITICAL_THRESHOLD_RULES"
        )


if __name__ == "__main__":
    unittest.main()
