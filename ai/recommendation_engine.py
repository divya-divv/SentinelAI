def generate_recommendations(event):
    """
    Generate recommended actions based on
    the operational event.
    """

    recommendations = []

    if event["cpu_usage"] >= 75:
        recommendations.append(
            "Investigate high CPU usage and consider scaling the service."
        )

    if event["memory_usage"] >= 75:
        recommendations.append(
            "Check memory consumption and investigate possible memory leaks."
        )

    if event["response_time_ms"] >= 500:
        recommendations.append(
            "Investigate slow response times and check service performance."
        )

    if event["error_rate"] >= 5:
        recommendations.append(
            "Review application errors and inspect recent service logs."
        )

    if event.get("is_anomaly"):
        recommendations.append(
            "Investigate the anomalous pattern before taking automated action."
        )

    if event.get("risk_level") == "CRITICAL":
        recommendations.append(
            "Escalate this event to the operations team for immediate review."
        )

    if not recommendations:
        recommendations.append(
            "No immediate action is required. Continue monitoring."
        )

    return recommendations