# SSH Monitor — Brute-Force Detection & Monitoring

![Tests](https://img.shields.io/badge/tests-14%20passed-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-97%25-brightgreen)
![Python](https://img.shields.io/badge/Python-3.14-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![Grafana](https://img.shields.io/badge/Grafana-Monitoring-orange)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)

A defensive cybersecurity monitoring project that detects **SSH brute-force login attempts**, stores security events in PostgreSQL, visualizes activity through Grafana, and generates alerts when suspicious login activity exceeds a defined threshold.

The project was developed and tested in a controlled cybersecurity laboratory environment using **Kali Linux as the attacker environment** and **Ubuntu WSL as the SSH server environment**.

---

## 📌 Project Overview

SSH Monitor is a lightweight security monitoring system designed to identify suspicious SSH authentication activity.

The system:

* Parses SSH authentication logs
* Detects repeated failed login attempts
* Identifies potential brute-force attacks
* Stores authentication events in PostgreSQL
* Provides Grafana dashboards for security monitoring
* Generates alerts for high-volume failed logins
* Includes automated unit tests
* Uses GitHub Actions for continuous integration
* Uses Kali Linux to simulate controlled SSH attacks

---

## 🏗️ System Architecture

```text
                  ┌──────────────────────┐
                  │      Kali Linux      │
                  │  Attacker / Testing  │
                  └──────────┬───────────┘
                             │
                             │ Controlled SSH
                             │ attack simulation
                             ▼
                  ┌──────────────────────┐
                  │     Ubuntu WSL       │
                  │     SSH Server       │
                  │      (Victim)        │
                  └──────────┬───────────┘
                             │
                             │ /var/log/auth.log
                             ▼
                  ┌──────────────────────┐
                  │    Python Monitor    │
                  │                      │
                  │ • Log Parser         │
                  │ • Brute-force        │
                  │   Detector           │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │     PostgreSQL       │
                  │   Security Events    │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │       Grafana        │
                  │      Dashboard       │
                  │                      │
                  │ • Failed Logins      │
                  │ • Attacking IPs      │
                  │ • Targeted Users     │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │    Security Alert    │
                  │   Brute-force Alert  │
                  └──────────────────────┘
```

---

## 🛠️ Technologies Used

| Technology     | Purpose                               |
| -------------- | ------------------------------------- |
| Python         | Log parsing and brute-force detection |
| PostgreSQL     | Security event storage                |
| Grafana        | Monitoring and visualization          |
| Docker Compose | Containerized PostgreSQL and Grafana  |
| Ubuntu WSL     | SSH server / victim environment       |
| Kali Linux     | Controlled attacker environment       |
| Hydra          | Controlled SSH brute-force simulation |
| Pytest         | Automated testing                     |
| Coverage       | Test coverage measurement             |
| Git & GitHub   | Version control                       |
| GitHub Actions | Continuous integration                |

---

## 📂 Project Structure

```text
ssh-monitor/
│
├── src/
│   ├── __init__.py
│   ├── parser.py
│   ├── detector.py
│   └── db.py
│
├── tests/
│   ├── __init__.py
│   ├── test_parser.py
│   ├── test_detector.py
│   └── data/
│       └── test_auth.log
│
├── sample_logs/
│   └── auth.log
│
├── docs/
│   └── screenshots/
│       ├── kali-attack.png
│       ├── grafana-dashboard.png
│       ├── grafana-alert.png
│       ├── attack-detection.png
│       ├── pytest-tests.png
│       └── github-actions.png
│
├── main.py
├── docker-compose.yml
├── INCIDENT.md
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/hashani/ssh-monitor
cd ssh-monitor
```

## 2. Create a Python Virtual Environment

On Windows PowerShell:

```powershell
python -m venv venv
```

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

The terminal should show:

```text
(venv) PS C:\Users\Acer\ssh-monitor>
```

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# 🐳 Docker Setup

Docker Compose is used to run PostgreSQL and Grafana.

Start the services:

```powershell
docker compose up -d
```

Check the containers:

```powershell
docker compose ps
```

The project uses:

* PostgreSQL — port `5432`
* Grafana — port `3000`

Grafana:

```text
http://localhost:3000
```

---

# 🔍 Running the Monitor

Run the monitoring application:

```powershell
python main.py
```

Example output:

```text
Parsed 34 events
ALERT: 172.18.xxx.xxx brute force, 28 failures, first seen ...
Saved to database
```

The application:

1. Reads the SSH authentication log.
2. Parses authentication events.
3. Detects repeated failed login attempts.
4. Stores events in PostgreSQL.
5. Reports potential brute-force attacks.

---

# 🧪 Testing

The project includes automated tests for the parser and brute-force detection logic.

Run:

```powershell
python -m pytest -v
```

Current result:

```text
14 passed
```

### Test Coverage

Coverage was measured using:

```powershell
coverage run -m pytest
coverage report
```

Current overall coverage:

```text
TOTAL    87    3    97%
```

| Component         | Coverage |
| ----------------- | -------: |
| `src/detector.py` |     100% |
| `src/parser.py`   |      89% |
| Overall           |  **97%** |

### Pytest Results

![Pytest Results](docs/screenshots/pytest-tests.png)

---

# 🐉 Kali Linux Attack Simulation

Kali Linux was used as the **attacker environment** to perform a controlled SSH brute-force simulation.

The attack was conducted only against the project's own Ubuntu WSL SSH server in a controlled laboratory environment.

The testing workflow was:

```text
Kali Linux
     │
     │ Controlled SSH attack
     ▼
Ubuntu WSL SSH Server
     │
     │ Authentication failures
     ▼
/var/log/auth.log
     │
     ▼
Python SSH Monitor
     │
     ▼
Brute-force Detection
```

A controlled password list was created for the test:

```bash
printf "wrongpass1\nwrongpass2\nwrongpass3\nwrongpass4\n" > wordlist.txt
```

For the brute-force detection test, multiple test passwords were generated:

```bash
for i in $(seq 1 25); do echo "wrongpass$i"; done > alert-test.txt
```

The controlled SSH test was performed using Hydra:

```bash
hydra -l acer -P alert-test.txt -t 1 ssh://<WSL-IP>
```

The generated authentication failures were recorded by the Ubuntu SSH server.

The authentication log was then copied into the monitoring project for analysis.

### Kali Linux Attack Screenshot

![Kali Linux Attack Simulation](docs/screenshots/kali-attack.png)

---

# 🚨 Brute-Force Detection

The detector identifies repeated failed SSH authentication attempts from the same IP address.

Example:

```text
ALERT: 172.18.xxx.xxx brute force, 28 failures
```

The configured detection threshold is:

```text
More than 20 failed SSH login attempts
from the same IP address
within 5 minutes
```

This threshold can be adjusted depending on the monitoring requirements.

---

# 🗄️ PostgreSQL Database

Authentication events are stored in PostgreSQL.

The `events` table contains:

| Column     | Description                    |
| ---------- | ------------------------------ |
| `id`       | Unique event ID                |
| `ts`       | Authentication event timestamp |
| `ip`       | Source IP address              |
| `username` | Target username                |
| `status`   | Authentication status          |

Authentication statuses include:

```text
Failed
Accepted
```

Duplicate event protection is implemented using a unique index based on:

```text
timestamp + IP + username + status
```

This prevents the same authentication event from being inserted multiple times.

---

# 📊 Grafana Monitoring

Grafana is used to visualize the SSH security events stored in PostgreSQL.

The dashboard contains three main panels.

### 1. Failed Logins Over Time

Displays failed SSH login activity over time.

### 2. Top Attacking IPs

Displays the IP addresses generating the highest number of failed login attempts.

### 3. Most Targeted Usernames

Displays usernames receiving the highest number of failed authentication attempts.

### Grafana Dashboard

![Grafana Dashboard](docs/screenshots/grafana-dashboard.png)

---

# 🚨 Grafana Alerting

A Grafana alert rule named:

```text
SSH Brute Force Detection
```

was configured to monitor SSH authentication activity.

The rule evaluates the number of failed SSH login attempts within a **5-minute window**.

Detection condition:

```text
Failed SSH attempts > 20
within 5 minutes
```

Alert labels:

```text
service=ssh
severity=critical
type=brute_force
```

Alert summary:

```text
SSH brute-force attack detected
```

Alert description:

```text
More than 20 failed SSH login attempts were detected
from an IP address within 5 minutes.
```

### Grafana Alert

![Grafana Alert](docs/screenshots/grafana-alert.png)

---

# 🔎 Attack Detection Evidence

The controlled attack generated multiple failed SSH authentication attempts.

The complete detection flow was:

```text
Kali Linux
    ↓
Controlled SSH Attack
    ↓
Ubuntu WSL SSH Server
    ↓
/var/log/auth.log
    ↓
Python Log Parser
    ↓
Brute-force Detector
    ↓
PostgreSQL
    ↓
Grafana
    ↓
SSH Brute-force Alert
```

### Detection Result

![Attack Detection](docs/screenshots/attack-detection.png)

---

# 🔄 Security Monitoring Workflow

```text
1. Kali Linux
       ↓
2. Controlled SSH Attack
       ↓
3. Ubuntu WSL SSH Server
       ↓
4. SSH Authentication Logs
       ↓
5. Python Log Parser
       ↓
6. Brute-force Detection
       ↓
7. PostgreSQL
       ↓
8. Grafana Dashboard
       ↓
9. Grafana Alert
       ↓
10. Security Response
```

---

# 🔁 Continuous Integration

GitHub Actions is used to automatically run the project's automated tests.

The CI workflow helps verify that changes to the project do not break the existing functionality.

### GitHub Actions

![GitHub Actions](docs/screenshots/github-actions.png)

---

# 📋 Incident Report

A detailed incident report documenting the controlled SSH brute-force attack, detection process, database evidence, Grafana monitoring, time synchronization issue, response, and lessons learned is available here:

[View the Incident Report](INCIDENT.md)

---

# 🎯 Key Learning Outcomes

This project provided practical experience in:

* SSH security monitoring
* Linux authentication logs
* Python log parsing
* Brute-force detection
* Cybersecurity incident detection
* PostgreSQL database management
* Grafana monitoring
* Security alert configuration
* Docker and Docker Compose
* Kali Linux
* Controlled security testing
* Ubuntu WSL
* Automated testing with Pytest
* Code coverage
* Git and GitHub
* GitHub Actions
* Continuous Integration
* Security incident documentation

---

# 🚀 Future Improvements

Possible future improvements include:

* Real-time SSH log monitoring
* Automatic malicious IP blocking
* Email and messaging notifications
* Advanced anomaly detection
* Machine-learning-based attack detection
* Support for additional authentication log formats
* IP reputation checking
* Geographic visualization of attacking IPs
* Role-based access control
* Containerized deployment of the complete monitoring application

---

# 🔐 Security Notice

This project is intended for **educational and defensive cybersecurity purposes**.

The attack simulation was performed only against systems controlled for this project.

Do not use SSH brute-force or security testing tools against systems, networks, accounts, or services without explicit authorization.

---

# 👩‍💻 Author

**Hashani**

Computer Science Undergraduate
University of Vavuniya

---

## ⭐ Project Summary

SSH Monitor demonstrates a complete defensive cybersecurity monitoring workflow:

```text
Kali Linux
     ↓
Controlled SSH Attack
     ↓
Ubuntu WSL
     ↓
SSH Authentication Logs
     ↓
Python Log Parser
     ↓
Brute-force Detection
     ↓
PostgreSQL
     ↓
Grafana
     ↓
Security Alert
```

The project combines **Kali Linux attack simulation, log analysis, brute-force detection, database storage, visualization, alerting, automated testing and continuous integration** into a practical defensive cybersecurity monitoring system.
