def explain_event(event):
    """
    Generate a human-readable explanation
    for an operational event.
    """

    reasons = []

    if event["cpu_usage"] >= 75:
        reasons.append(
            f"High CPU usage detected ({event['cpu_usage']}%)."
        )

    if event["memory_usage"] >= 75:
        reasons.append(
            f"High memory usage detected ({event['memory_usage']}%)."
        )

    if event["response_time_ms"] >= 500:
        reasons.append(
            f"Slow response time detected ({event['response_time_ms']} ms)."
        )

    if event["error_rate"] >= 5:
        reasons.append(
            f"Elevated error rate detected ({event['error_rate']}%)."
        )

    if event.get("is_anomaly"):
        reasons.append(
            "Machine learning detected an unusual operational pattern."
        )

    if not reasons:
        reasons.append(
            "No significant operational issues were detected."
        )

    return {
        "summary": " ".join(reasons),
        "reasons": reasons
    }