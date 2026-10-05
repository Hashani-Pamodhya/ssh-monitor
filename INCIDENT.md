# SSH Brute-Force Attack — Incident Report

**Incident ID:** SSH-2026-001
**Date:** 05 October 2026
**Severity:** High
**Status:** Resolved
**Environment:** Private Cybersecurity Lab

---

## 1. Executive Summary

A controlled SSH brute-force attack was conducted against a test Ubuntu SSH server to validate the functionality of the **SSH Monitoring and Detection System**.

The attack was generated from a Kali Linux virtual machine using Hydra and targeted the SSH service of an Ubuntu environment running under WSL. The monitoring system successfully collected the authentication logs, detected repeated failed login attempts, stored the events in PostgreSQL, visualized the activity through Grafana, and triggered a brute-force security alert.

A total of **28 failed SSH authentication attempts** were detected from the attacking host. The Grafana alert correctly entered the **Firing** state and subsequently returned to **Normal** after the attack activity stopped and the events fell outside the five-minute detection window.

The experiment was performed exclusively against systems controlled by the researcher.

---

## 2. Incident Details

| Field               | Details                                |
| ------------------- | -------------------------------------- |
| Incident Type       | SSH Brute-Force Attack                 |
| Severity            | High                                   |
| Status              | Resolved                               |
| Attacker            | Kali Linux VM                          |
| Victim              | Ubuntu SSH Server (WSL)                |
| Attack Tool         | Hydra                                  |
| Protocol            | SSH                                    |
| Target Account      | `acer`                                 |
| Source IP           | `172.18.247.45`                        |
| Detected Failures   | 28                                     |
| Detection Threshold | More than 20 failures within 5 minutes |
| Monitoring          | Python + PostgreSQL + Grafana          |

---

## 3. Environment

The experiment was conducted using the following architecture:

```text
┌─────────────────────┐
│    Kali Linux VM    │
│      ATTACKER       │
│                     │
│       Hydra         │
└──────────┬──────────┘
           │
           │ SSH
           │ Controlled
           │ Attack
           ▼
┌─────────────────────┐
│     WSL Ubuntu      │
│       VICTIM        │
│                     │
│    SSH Service      │
│    auth.log         │
└──────────┬──────────┘
           │
           │ Log Collection
           ▼
┌─────────────────────┐
│   Python Monitor    │
│                     │
│ Parser + Detector   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     PostgreSQL      │
│    Event Storage    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│       Grafana       │
│                     │
│ Dashboard + Alert   │
└─────────────────────┘
```

---

## 4. Attack Description

A password-based SSH brute-force attack was simulated against the test Ubuntu SSH server.

Hydra was used to generate repeated authentication failures against the `acer` account. The attack was intentionally limited to the researcher's own laboratory environment.

The SSH server recorded the authentication failures in:

```text
/var/log/auth.log
```

The log was subsequently collected and supplied to the monitoring system for analysis.

---

## 5. Detection

The monitoring system uses a Python parser to extract security-relevant information from SSH authentication logs, including:

* Timestamp
* Source IP address
* Username
* Authentication status

The brute-force detection component analyzes repeated failed authentication attempts.

During the test, the detector generated:

```text
ALERT: 172.18.247.45 brute force,
28 failures
```

This confirmed that the monitoring system successfully identified the simulated brute-force activity.

---

## 6. Database Evidence

The detected events were stored in PostgreSQL.

The database showed:

```text
Source IP       Status    Count
--------------------------------
172.18.247.45   Failed      28
```

Additional protections were implemented to prevent duplicate events from being stored.

A unique index was created using:

```text
(ts, ip, username, status)
```

After duplicate cleanup and verification, the database contained:

```text
44 unique events
```

---

## 7. Grafana Monitoring

Grafana was configured as the monitoring and visualization layer.

The dashboard provides visibility into:

### Failed Logins Over Time

Shows the number of failed SSH authentication attempts over time.

### Top Attacking IPs

The controlled attack was identified as:

```text
172.18.247.45 — 28 failed attempts
```

### Most Targeted Usernames

The attack targeted:

```text
acer
```

This dashboard provides a visual representation of suspicious SSH authentication activity.

---

## 8. Alert Detection

A Grafana alert named:

```text
SSH Brute Force Detection
```

was configured with the following rule:

```text
More than 20 failed SSH login attempts
from an IP address within 5 minutes
```

During the simulated attack:

```text
28 failures
     ↓
Threshold exceeded
     ↓
🔴 ALERT FIRING
```

After the attack stopped:

```text
No new failures within 5 minutes
     ↓
Threshold no longer exceeded
     ↓
🟢 ALERT NORMAL
```

This confirmed both **attack detection** and **alert recovery**.

---

## 9. Time Synchronization Issue

During testing, the alert initially remained in the `Firing` state because the PostgreSQL database was using UTC while the collected SSH log timestamps represented Sri Lankan local time.

The issue was resolved by configuring PostgreSQL to use:

```text
Asia/Colombo
```

The event timestamp column was also converted from:

```text
timestamp without time zone
```

to:

```text
timestamp with time zone
```

After the correction, the five-minute detection window worked correctly and the alert successfully returned to the `Normal` state.

---

## 10. Incident Response

### Detection

The repeated failed SSH authentication attempts were identified by the Python brute-force detection component.

### Analysis

The events were stored in PostgreSQL and examined through Grafana. The source IP `172.18.247.45` generated 28 failed authentication attempts against the `acer` account.

### Containment

The activity was generated intentionally as part of a controlled security test. No external system was affected.

### Recovery

After the attack stopped, the monitoring system continued evaluating the five-minute detection window. Once the attack events were outside that window, the Grafana alert automatically returned to `Normal`.

---

## 11. Recommended Preventive Measures

For a production SSH server, the following controls are recommended:

### SSH Key-Based Authentication

Use public-key authentication instead of password authentication where possible.

### Disable Password Authentication

After confirming key-based authentication works correctly, password-based SSH authentication can be disabled.

### Disable Direct Root Login

Direct SSH access to the root account should be disabled.

```text
PermitRootLogin no
```

### Fail2ban

Deploy Fail2ban to automatically block IP addresses that generate repeated failed SSH authentication attempts.

### Monitoring and Alerting

Continue monitoring SSH authentication logs and maintain alerts for abnormal authentication activity.

### Network Restrictions

Where possible, restrict SSH access to trusted networks, VPNs, or specific administrative IP addresses.

---

## 12. Lessons Learned

The experiment demonstrated several important aspects of security monitoring:

1. Authentication logs provide valuable evidence for detecting brute-force attacks.
2. Repeated failures from a single source can be detected using threshold-based analysis.
3. Centralized event storage makes security data easier to investigate.
4. Grafana provides useful real-time visualization and alerting capabilities.
5. Correct timestamp and timezone handling is essential for time-based security detection.
6. Duplicate-event protection is important when repeatedly processing log files.
7. Automated alert recovery is important so that resolved incidents do not remain permanently active.

---

## 13. Final Outcome

The SSH monitoring system successfully completed the end-to-end detection workflow:

```text
SSH Attack
    ↓
Authentication Logs
    ↓
Python Log Parser
    ↓
Brute-Force Detection
    ↓
PostgreSQL
    ↓
Grafana Dashboard
    ↓
Security Alert
    ↓
Firing
    ↓
Attack Stops
    ↓
Normal
```

The controlled experiment successfully validated the system's ability to detect and monitor SSH brute-force activity.

**Final result: SUCCESSFUL DETECTION AND RECOVERY**

---

> **Security Notice:** This incident was a controlled security experiment performed only against systems owned or controlled by the researcher. No third-party systems were targeted.
