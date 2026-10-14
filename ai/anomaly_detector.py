from sklearn.ensemble import IsolationForest


class AnomalyDetector:

    def __init__(self):
        self.model = IsolationForest(
            n_estimators=200,
            contamination=0.15,
            random_state=42
        )

        self.is_trained = False

    def train(self, events):
        if len(events) < 10:
            print(
                f"AI MODEL: Not enough data. Events = {len(events)}"
            )
            return False

        data = [
            [
                float(event["cpu_usage"]),
                float(event["memory_usage"]),
                float(event["response_time_ms"]),
                float(event["error_rate"])
            ]
            for event in events
        ]

        self.model.fit(data)
        self.is_trained = True

        print(
            f"AI MODEL TRAINED SUCCESSFULLY using {len(events)} events"
        )

        return True

    def predict(self, event):
        data = [[
            float(event["cpu_usage"]),
            float(event["memory_usage"]),
            float(event["response_time_ms"]),
            float(event["error_rate"])
        ]]

        if self.is_trained:
            prediction = self.model.predict(data)
            score = float(
                self.model.decision_function(data)[0]
            )

            # Convert NumPy Boolean to standard Python bool
            ai_anomaly = bool(prediction[0] == -1)

        else:
            score = 0.0
            ai_anomaly = False

        extreme_condition = bool(
            float(event["cpu_usage"]) >= 95
            or float(event["memory_usage"]) >= 95
            or float(event["response_time_ms"]) >= 2000
            or float(event["error_rate"]) >= 20
        )

        is_anomaly = bool(
            ai_anomaly or extreme_condition
        )

        if ai_anomaly and extreme_condition:
            detection_method = "MACHINE_LEARNING_AND_RULES"
        elif ai_anomaly:
            detection_method = "MACHINE_LEARNING"
        elif extreme_condition:
            detection_method = "CRITICAL_THRESHOLD_RULES"
        else:
            detection_method = "NONE"

        print(
            f"ANOMALY DETECTION: {detection_method}, "
            f"anomaly={is_anomaly}, score={score:.4f}"
        )

        return {
            "is_anomaly": is_anomaly,
            "anomaly_score": round(score, 4),
            "ai_anomaly": ai_anomaly,
            "extreme_condition": extreme_condition,
            "detection_method": detection_method,
            "model_trained": bool(self.is_trained)
        }