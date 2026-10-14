def calculate_risk(event):
    """
    Calculate an operational risk score and classify the risk level.
    """

    risk_score = 0

    # CPU usage
    if event["cpu_usage"] >= 90:
        risk_score += 40
    elif event["cpu_usage"] >= 75:
        risk_score += 20

    # Memory usage
    if event["memory_usage"] >= 90:
        risk_score += 30
    elif event["memory_usage"] >= 75:
        risk_score += 15

    # Response time
    if event["response_time_ms"] >= 800:
        risk_score += 30
    elif event["response_time_ms"] >= 500:
        risk_score += 15

    # Error rate
    if event["error_rate"] >= 10:
        risk_score += 40
    elif event["error_rate"] >= 5:
        risk_score += 20

    # Classify risk
    if risk_score >= 80:
        risk_level = "CRITICAL"
    elif risk_score >= 30:
        risk_level = "WARNING"
    else:
        risk_level = "NORMAL"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level
    }