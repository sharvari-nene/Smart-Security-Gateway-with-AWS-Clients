from flask import Flask, request
import time

app = Flask(__name__)

SECRET_KEY = "mysecret"

RATE_LIMIT = 5
TIME_WINDOW = 60
BAN_TIME = 60
FAIL_THRESHOLD = 3

request_log = {}
blocked_ips = {}
failed_attempts = {}
logs = []

@app.route('/')
def home():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    if "," in ip:
        ip = ip.split(",")[0].strip()
    current_time = time.time()

    if ip in blocked_ips:
        if current_time < blocked_ips[ip]:
            logs.append({
                "ip": ip,
                "time": current_time,
                "status": "blocked",
                "reason": "temporary_ban"
            })
            print(f"{ip} → TEMP BANNED")
            return {"message": "IP temporarily banned"}, 403
        else:
            del blocked_ips[ip]
            failed_attempts[ip] = 0

    key = request.headers.get("X-Access-Key")
    if key != SECRET_KEY:
        failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
        logs.append({
            "ip": ip,
            "time": current_time,
            "status": "blocked",
            "reason": "invalid_header"
        })
        print(f"{ip} → FAILED AUTH ({failed_attempts[ip]})")
        if failed_attempts[ip] >= FAIL_THRESHOLD:
            blocked_ips[ip] = current_time + BAN_TIME
            print(f"{ip} → BANNED")
        return {"message": "Access Denied"}, 403

    if ip not in request_log:
        request_log[ip] = []

    request_log[ip] = [
        t for t in request_log[ip]
        if current_time - t < TIME_WINDOW
    ]

    if len(request_log[ip]) >= RATE_LIMIT:
        failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
        logs.append({
            "ip": ip,
            "time": current_time,
            "status": "blocked",
            "reason": "rate_limit"
        })
        print(f"{ip} → RATE LIMIT HIT ({failed_attempts[ip]})")
        if failed_attempts[ip] >= FAIL_THRESHOLD:
            blocked_ips[ip] = current_time + BAN_TIME
            print(f"{ip} → BANNED")
        return {"message": "Rate limit exceeded"}, 429

    request_log[ip].append(current_time)
    failed_attempts[ip] = 0

    logs.append({
        "ip": ip,
        "time": current_time,
        "status": "allowed",
        "reason": "success"
    })

    print(f"{ip} → ALLOWED")

    return {"message": "Access Granted"}

@app.route('/api/logs')
def api_logs():
    return {
        "logs": logs[-20:],
        "blocked_ips": list(blocked_ips.keys())
    }

@app.route('/logs')
def get_logs():
    return """
    <html>
    <head>
        <title>Gateway Dashboard</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #1e293b, #0f172a);
                color: #e2e8f0;
                margin: 0;
                padding: 20px;
            }
            h1 {
                text-align: center;
            }
            .container {
                max-width: 1000px;
                margin: auto;
            }
            .stats {
                display: flex;
                justify-content: space-between;
                margin-bottom: 20px;
            }
            .card {
                flex: 1;
                margin: 5px;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                background: #1e293b;
                box-shadow: 0 4px 10px rgba(0,0,0,0.4);
            }
            .allowed { color: #22c55e; font-weight: bold; }
            .blocked { color: #ef4444; font-weight: bold; }
            .banned { background-color: rgba(239,68,68,0.2); }
            table {
                width: 100%;
                border-collapse: collapse;
                background: #1e293b;
                border-radius: 10px;
                overflow: hidden;
            }
            th, td {
                padding: 12px;
                text-align: center;
            }
            th {
                background: #334155;
            }
            tr:nth-child(even) {
                background: #0f172a;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Smart Security Gateway</h1>

            <div class="stats">
                <div class="card"><h2 id="total">0</h2><p>Total</p></div>
                <div class="card"><h2 id="allowed">0</h2><p>Allowed</p></div>
                <div class="card"><h2 id="blocked">0</h2><p>Blocked</p></div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>IP</th>
                        <th>Time</th>
                        <th>Status</th>
                        <th>Reason</th>
                    </tr>
                </thead>
                <tbody id="logTable"></tbody>
            </table>
        </div>

        <script>
            async function fetchLogs() {
                const res = await fetch('/api/logs');
                const data = await res.json();

                const logs = data.logs;
                const blockedIPs = data.blocked_ips;

                let allowed = 0;
                let blocked = 0;

                const table = document.getElementById("logTable");
                table.innerHTML = "";

                logs.forEach(log => {
                    if (log.status === "allowed") allowed++;
                    else blocked++;

                    const row = document.createElement("tr");

                    if (blockedIPs.includes(log.ip)) {
                        row.classList.add("banned");
                    }

                    row.innerHTML = `
                        <td>${log.ip}</td>
                        <td>${new Date(log.time * 1000).toLocaleTimeString()}</td>
                        <td class="${log.status}">${log.status}</td>
                        <td>${log.reason}</td>
                    `;

                    table.appendChild(row);
                });

                document.getElementById("total").innerText = logs.length;
                document.getElementById("allowed").innerText = allowed;
                document.getElementById("blocked").innerText = blocked;
            }

            setInterval(fetchLogs, 2000);
            fetchLogs();
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)