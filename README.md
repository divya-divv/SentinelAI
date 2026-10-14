\# SentinelAI — AI-Powered Operations Monitoring Platform



SentinelAI is a full-stack AI operations monitoring platform designed to analyze service events, identify potential anomalies, assess operational risks, and present insights through an interactive dashboard.



The project combines machine learning, backend APIs, database persistence, and a React frontend to demonstrate how AI can support monitoring and operational decision-making.



\## Key Features



\* \*\*AI Anomaly Detection:\*\* Uses the Isolation Forest machine learning algorithm to identify unusual service behavior.

\* \*\*Risk Assessment:\*\* Evaluates operational events and classifies their severity as Normal, Warning, or Critical.

\* \*\*Event Processing:\*\* Accepts service monitoring events through a FastAPI backend.

\* \*\*Interactive Dashboard:\*\* Displays event statistics, severity categories, and detected anomalies.

\* \*\*Database Persistence:\*\* Uses SQLAlchemy and SQLite to store event information.

\* \*\*Event Simulator:\*\* Generates sample service events for testing and demonstration.

\* \*\*Explanations and Recommendations:\*\* Provides insights to help users understand potential operational issues.

\* \*\*Automated Testing:\*\* Includes tests for anomaly detection, risk classification, and event processing.



\## Technology Stack



| Component            | Technologies                   |

| -------------------- | ------------------------------ |

| Programming Language | Python, JavaScript             |

| Backend              | FastAPI                        |

| Frontend             | React, Vite                    |

| Database             | SQLite                         |

| Database Integration | SQLAlchemy                     |

| Machine Learning     | Scikit-learn, Isolation Forest |

| Testing              | Pytest                         |

| Version Control      | Git, GitHub                    |



\## How It Works



1\. \*\*Event Collection:\*\* The backend receives operational metrics such as CPU usage, memory usage, response time, and error rate.

2\. \*\*Risk Analysis:\*\* The risk engine evaluates event metrics and assigns a severity level.

3\. \*\*Anomaly Detection:\*\* The Isolation Forest model analyzes event patterns to identify unusual behavior.

4\. \*\*Data Storage:\*\* Event information is stored in the database.

5\. \*\*Dashboard Visualization:\*\* The frontend presents event statistics and monitoring results.

6\. \*\*Operational Insights:\*\* Explanations and recommendations help users investigate potential problems.



\## Project Structure



```text

SentinelAI/

├── ai/

│   ├── anomaly\_detector.py

│   ├── explanation\_engine.py

│   ├── recommendation\_engine.py

│   └── risk\_engine.py

├── backend/

│   ├── main.py

│   └── simulator.py

├── database/

│   ├── database.py

│   ├── init\_db.py

│   └── models.py

├── frontend/

│   ├── src/

│   ├── package.json

│   └── vite.config.js

├── tests/

│   ├── test\_anomaly\_detector.py

│   ├── test\_event\_workflow.py

│   └── test\_risk\_engine.py

├── .gitignore

└── README.md

```



\## Getting Started



\### Prerequisites



Install the following before running the project:



\* Python

\* Node.js and npm

\* Git



\### 1. Clone the Repository



Replace `<repository-url>` with the URL of this GitHub repository.



```bash

git clone <repository-url>

cd SentinelAI

```



\### 2. Set Up the Python Environment



Create a virtual environment:



```bash

python -m venv .venv

```



Activate it on Windows PowerShell:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



Install the Python packages required by the project. Use the project's dependency file if one is available.



\### 3. Start the Backend



From the project root, run:



```bash

python -m uvicorn backend.main:app --reload

```



The backend should be available at:



`http://127.0.0.1:8000`



The FastAPI interactive API documentation is normally available at:



`http://127.0.0.1:8000/docs`



\### 4. Start the Frontend



Open a second terminal:



```powershell

cd frontend

npm install

npm run dev

```



Open the local development URL printed by Vite in your terminal.



Make sure the frontend's configured API URL and the backend's CORS settings match your local setup.



\## Running the Tests



From the project root, activate the virtual environment and run:



```bash

python -m pytest tests -v

```



\### Current Test Results



\*\*8 tests passed\*\*



The tests cover:



\* Anomaly detector training and predictions

\* Detection of extreme conditions

\* Risk classification

\* Event processing workflow



\## Project Goals



SentinelAI was developed to explore the practical application of machine learning in operations monitoring. It combines software engineering and AI techniques in a working full-stack project.



The project demonstrates experience with:



\* REST API development

\* Machine learning integration

\* Database design and persistence

\* Frontend and backend integration

\* Automated testing

\* Git-based version control



\## Future Improvements



Potential enhancements include:



\* Real-time event streaming

\* Historical monitoring charts

\* Configurable alert thresholds

\* Advanced event filtering and search

\* Authentication and role-based access control

\* Deployment and production monitoring integrations



\## Author



\*\*Divya J\*\*



Computer Science Engineering Student | AI \& Full-Stack Development



GitHub: `divya-divv`



\---



\*SentinelAI is an educational and portfolio project. Detection results should be validated before being used for critical operational decisions.\*



