import unittest
from ai.risk_engine import calculate_risk


class TestRiskEngine(unittest.TestCase):

    def test_normal_event(self):
        event = {
            "cpu_usage": 10,
            "memory_usage": 20,
            "response_time_ms": 100,
            "error_rate": 0
        }

        result = calculate_risk(event)

        self.assertEqual(result["risk_level"], "NORMAL")
        self.assertEqual(result["risk_score"], 0)

    def test_warning_event(self):
        event = {
            "cpu_usage": 80,
            "memory_usage": 78,
            "response_time_ms": 600,
            "error_rate": 6
        }

        result = calculate_risk(event)

        self.assertEqual(result["risk_level"], "WARNING")
        self.assertEqual(result["risk_score"], 70)

    def test_critical_event(self):
        event = {
            "cpu_usage": 96,
            "memory_usage": 96,
            "response_time_ms": 4200,
            "error_rate": 22
        }

        result = calculate_risk(event)

        self.assertEqual(result["risk_level"], "CRITICAL")
        self.assertEqual(result["risk_score"], 140)


if __name__ == "__main__":
    unittest.main()
