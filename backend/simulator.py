import random
import time
import requests
from datetime import datetime

BACKEND_URL = "http://127.0.0.1:8001/events"


def generate_event():
    event = {
        "timestamp": datetime.now().isoformat(),
        "service": random.choice(
            ["payment-service", "user-service", "api-service"]
        ),
        "cpu_usage": round(random.uniform(20, 95), 2),
        "memory_usage": round(random.uniform(30, 95), 2),
        "response_time_ms": round(random.uniform(100, 900), 2),
        "error_rate": round(random.uniform(0, 12), 2),
    }

    return event


if __name__ == "__main__":
    print("========================================")
    print("   SentinelAI Real-Time Event Engine")
    print("========================================")
    print("Sending events to SentinelAI backend...\n")

    while True:
        event = generate_event()

        try:
            response = requests.post(
                BACKEND_URL,
                json=event,
                timeout=5
            )

            if response.status_code == 200:
                result = response.json()
                analyzed_event = result["event"]

                print("Service:", analyzed_event["service"])
                print("CPU:", analyzed_event["cpu_usage"], "%")
                print("Memory:", analyzed_event["memory_usage"], "%")
                print(
                    "Response Time:",
                    analyzed_event["response_time_ms"],
                    "ms"
                )
                print(
                    "Error Rate:",
                    analyzed_event["error_rate"],
                    "%"
                )
                print(
                    "Risk Score:",
                    analyzed_event["risk_score"]
                )
                print(
                    "Risk Level:",
                    analyzed_event["risk_level"]
                )
                print(
                    "Is Anomaly:",
                    analyzed_event["is_anomaly"]
                )
                print(
                    "Anomaly Score:",
                    analyzed_event["anomaly_score"]
                )
                print("----------------------------------------")

            else:
                print(
                    "Backend returned an error:",
                    response.status_code
                )

        except requests.exceptions.RequestException:
            print("Could not connect to SentinelAI backend.")

        time.sleep(2)
