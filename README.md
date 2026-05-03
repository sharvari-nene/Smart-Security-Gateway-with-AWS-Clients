# Smart-Security-Gateway-with-AWS-Clients
Smart Security Gateway built using Flask that implements API protection with rate limiting, IP blocking, authentication headers, and real-time monitoring dashboard.

## 📌 Introduction

This project implements a **Smart Security Gateway** using Flask that protects APIs from unauthorized access, excessive requests, and malicious behavior.

It simulates a lightweight **API Gateway** with security features similar to production systems.

---

## 🎯 Objectives

* Secure API endpoints using authentication headers
* Prevent abuse using rate limiting
* Detect and block suspicious IPs
* Provide real-time monitoring dashboard

---

## ⚙️ Features

* ✅ API Key Authentication (`X-Access-Key`)
* ✅ Rate Limiting (requests per minute)
* ✅ Temporary IP Blocking (auto-ban system)
* ✅ Failed Attempt Tracking
* ✅ Live Logs Dashboard (HTML UI)
* ✅ REST API for logs (`/api/logs`)
* ✅ Reverse Proxy IP handling (`X-Forwarded-For`)

---

## 🛠️ Tech Stack

* Python
* Flask
* HTML, CSS, JavaScript

---

## 📂 Project Structure

```
project/
│── app.py   # Main Flask application
│── README.md
```

---

## 🚀 How It Works

1. Client sends request with header:

   ```
   X-Access-Key: mysecret
   ```
2. System checks:

   * Authentication
   * Rate limit
   * Failed attempts
3. If rules are violated:

   * Request is blocked
   * IP may be temporarily banned
4. Logs are stored and shown in dashboard

---

## 🔑 Configuration

You can modify:

```python
SECRET_KEY = "mysecret"
RATE_LIMIT = 5
TIME_WINDOW = 60
BAN_TIME = 60
FAIL_THRESHOLD = 3
```

---

## ▶️ How to Run

### 1. Install dependencies

```
pip install flask
```

### 2. Run the application

```
python app.py
```

### 3. Open in browser

```
http://localhost:5000/
```

### 4. View dashboard

```
http://localhost:5000/logs
```

---

## 🧪 API Endpoints

### Home

```
GET /
```

### Logs API

```
GET /api/logs
```

---

## 📊 Dashboard

* Shows allowed vs blocked requests
* Displays recent logs
* Highlights banned IPs

---

## 🔐 Security Mechanisms

* Header-based authentication
* Sliding window rate limiting
* Auto IP banning after repeated violations
* Request logging for monitoring

---

## 📈 Future Enhancements

* Integration with AWS API Gateway / WAF
* Database logging (MongoDB / MySQL)
* JWT-based authentication
* Distributed rate limiting using Redis
* Docker deployment

---

## ✅ Conclusion

This project demonstrates how core API security concepts like authentication, rate limiting, and monitoring can be implemented in a simple yet effective way using Flask.

---

## 👨‍💻 Contributors

* Shiv Nand
* Sharvari Nene
* Deep Lalwani
* Rugved Dhamane

---
