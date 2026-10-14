import { useEffect, useState, useCallback } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8001";
const REFRESH_INTERVAL = 3000;

function App() {
  const [dashboard, setDashboard] = useState({
    total_events: 0,
    normal_events: 0,
    warning_events: 0,
    critical_events: 0,
    anomalies: 0,
  });

  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [backendOnline, setBackendOnline] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  const loadDashboard = useCallback(async () => {
    try {
      const [dashboardResponse, eventsResponse] = await Promise.all([
        fetch(`${API_URL}/dashboard`),
        fetch(`${API_URL}/events`),
      ]);

      if (!dashboardResponse.ok || !eventsResponse.ok) {
        throw new Error("Backend request failed.");
      }

      const dashboardData = await dashboardResponse.json();
      const eventsData = await eventsResponse.json();

      setDashboard(dashboardData);
      setEvents(Array.isArray(eventsData.events) ? eventsData.events : []);
      setBackendOnline(true);
      setLastUpdated(new Date());
      setErrorMessage("");
    } catch (error) {
      console.error("SentinelAI connection error:", error);
      setBackendOnline(false);
      setErrorMessage(
        "Unable to connect to SentinelAI. Checking the connection again..."
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    let active = true;
    let timeoutId;

    const refreshDashboard = async () => {
      await loadDashboard();

      if (active) {
        timeoutId = setTimeout(refreshDashboard, REFRESH_INTERVAL);
      }
    };

    refreshDashboard();

    return () => {
      active = false;
      clearTimeout(timeoutId);
    };
  }, [loadDashboard]);

  const getRiskClass = (riskLevel) => {
    if (riskLevel === "CRITICAL") return "critical";
    if (riskLevel === "WARNING") return "warning";
    return "normal";
  };

  const getRiskMessage = (event) => {
    if (!event) {
      return "Waiting for operational data.";
    }

    if (event.risk_level === "CRITICAL") {
      return "Immediate attention recommended. SentinelAI has identified a high-risk infrastructure condition.";
    }

    if (event.risk_level === "WARNING") {
      return "Monitoring recommended. SentinelAI has detected abnormal infrastructure behavior.";
    }

    return "Infrastructure appears stable. No immediate intervention is required.";
  };

  const latestEvent = events[0];

  return (
    <div className="app">
      <header className="topbar">
        <div>
          <h1>🛡️ SentinelAI</h1>
          <p>Real-Time AI Operations Platform</p>
        </div>

        <div className="system-status">
          <span
            className={`status-dot ${
              backendOnline ? "online" : "offline"
            }`}
          />

          {backendOnline ? "System Online" : "Backend Offline"}
        </div>
      </header>

      <main className="dashboard">
        <section className="hero">
          <div>
            <h2>AI Operations Dashboard</h2>
            <p>
              Monitor infrastructure health, detect anomalies, analyze risks
              and receive AI-powered recommendations.
            </p>

            {lastUpdated && (
              <small>
                Last updated: {lastUpdated.toLocaleTimeString()}
              </small>
            )}
          </div>

          <button onClick={loadDashboard} disabled={loading}>
            ↻ Refresh
          </button>
        </section>

        {errorMessage && (
          <div className="empty-state" role="status">
            {errorMessage}
          </div>
        )}

        <section className="stats-grid">
          <div className="stat-card">
            <span className="stat-icon">📊</span>
            <div>
              <p>Total Events</p>
              <h3>{dashboard.total_events}</h3>
            </div>
          </div>

          <div className="stat-card normal-card">
            <span className="stat-icon">🟢</span>
            <div>
              <p>Normal</p>
              <h3>{dashboard.normal_events}</h3>
            </div>
          </div>

          <div className="stat-card warning-card">
            <span className="stat-icon">🟡</span>
            <div>
              <p>Warnings</p>
              <h3>{dashboard.warning_events}</h3>
            </div>
          </div>

          <div className="stat-card critical-card">
            <span className="stat-icon">🔴</span>
            <div>
              <p>Critical</p>
              <h3>{dashboard.critical_events}</h3>
            </div>
          </div>

          <div className="stat-card anomaly-card">
            <span className="stat-icon">🤖</span>
            <div>
              <p>AI Anomalies</p>
              <h3>{dashboard.anomalies}</h3>
            </div>
          </div>
        </section>

        <section className="events-section">
          <div className="section-header">
            <div>
              <h2>Recent Operational Events</h2>
              <p>Live events analyzed by SentinelAI</p>
            </div>

            <span className="live-badge">● LIVE</span>
          </div>

          {loading ? (
            <div className="empty-state">Loading SentinelAI data...</div>
          ) : events.length === 0 ? (
            <div className="empty-state">No events available yet.</div>
          ) : (
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Service</th>
                    <th>CPU</th>
                    <th>Memory</th>
                    <th>Response</th>
                    <th>Error Rate</th>
                    <th>Risk</th>
                    <th>AI Anomaly</th>
                  </tr>
                </thead>

                <tbody>
                  {events.slice(0, 20).map((event) => (
                    <tr key={event.id}>
                      <td>#{event.id}</td>
                      <td>
                        <strong>{event.service}</strong>
                      </td>
                      <td>{event.cpu_usage}%</td>
                      <td>{event.memory_usage}%</td>
                      <td>{event.response_time_ms} ms</td>
                      <td>{event.error_rate}%</td>

                      <td>
                        <span
                          className={`risk-badge ${getRiskClass(
                            event.risk_level
                          )}`}
                        >
                          {event.risk_level}
                        </span>
                      </td>

                      <td>
                        {event.is_anomaly ? (
                          <span className="anomaly-yes">⚠ Detected</span>
                        ) : (
                          <span className="anomaly-no">✓ Normal</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        {latestEvent && (
          <section className="analysis-section">
            <div className="section-header">
              <div>
                <h2>🤖 AI Risk Analysis</h2>
                <p>
                  Intelligent assessment of the latest infrastructure event
                </p>
              </div>

              <span
                className={`risk-badge ${getRiskClass(
                  latestEvent.risk_level
                )}`}
              >
                {latestEvent.risk_level}
              </span>
            </div>

            <div className="analysis-grid">
              <div className="analysis-card">
                <h3>🎯 Risk Assessment</h3>

                <div className="analysis-risk-level">
                  {latestEvent.risk_level}
                </div>

                <div className="risk-score">
                  Risk Score: {latestEvent.risk_score}
                </div>

                <p>{getRiskMessage(latestEvent)}</p>
              </div>

              <div className="analysis-card">
                <h3>🧠 AI Explanation</h3>

                <p>
                  {latestEvent.explanation ||
                    "SentinelAI is analyzing the current infrastructure behavior."}
                </p>

                <div className="analysis-metrics">
                  <span>
                    CPU: <strong>{latestEvent.cpu_usage}%</strong>
                  </span>

                  <span>
                    Memory: <strong>{latestEvent.memory_usage}%</strong>
                  </span>

                  <span>
                    Response:{" "}
                    <strong>{latestEvent.response_time_ms} ms</strong>
                  </span>

                  <span>
                    Errors: <strong>{latestEvent.error_rate}%</strong>
                  </span>
                </div>
              </div>

              <div className="analysis-card">
                <h3>⚡ Recommended Actions</h3>

                {Array.isArray(latestEvent.recommendations) &&
                latestEvent.recommendations.length > 0 ? (
                  <ul>
                    {latestEvent.recommendations.map((recommendation, index) => (
                      <li key={`${index}-${recommendation}`}>
                        {recommendation}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p>No immediate action required.</p>
                )}
              </div>
            </div>

            <div className="ai-summary">
              <span className="ai-summary-icon">🤖</span>

              <div>
                <h3>SentinelAI Decision</h3>

                <p>
                  Based on the latest infrastructure metrics, SentinelAI
                  classified this event as{" "}
                  <strong>{latestEvent.risk_level}</strong> risk with a score
                  of <strong>{latestEvent.risk_score}</strong>. The dashboard
                  checks for updated information every three seconds.
                </p>
              </div>
            </div>
          </section>
        )}
      </main>

      <footer>
        <p>SentinelAI • AI-Powered Infrastructure Monitoring</p>
      </footer>
    </div>
  );
}

export default App;