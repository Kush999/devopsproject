from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import psutil
import datetime
import os

app = Flask(__name__)

# This one line adds Prometheus metrics to your Flask app
# It automatically tracks:
#   - Request count per endpoint
#   - Request duration (how long each request takes)
#   - Response status codes
metrics = PrometheusMetrics(app)

# Custom metrics YOU define
# Counter: only goes up (like a request counter)
from prometheus_client import Counter, Gauge, Histogram

# Track how many times /health was called
health_checks = Counter(
    'health_check_total',
    'Total number of health checks'
)

# Track current CPU usage (can go up and down)
cpu_usage = Gauge(
    'app_cpu_usage_percent',
    'Current CPU usage percentage'
)

# Track request size distribution
request_duration = Histogram(
    'app_request_duration_seconds',
    'Request duration in seconds',
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5]
)

START_TIME = datetime.datetime.now()

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>DevOps Portfolio</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: 50px auto;
                padding: 20px;
                background-color: #0a0a0a;
                color: #e0e0e0;
            }
            h1 { color: #00d4ff; border-bottom: 2px solid #00d4ff; padding-bottom: 10px; }
            h2 { color: #00d4ff; }
            .card { background: #1a1a2e; border: 1px solid #16213e; border-radius: 8px; padding: 20px; margin: 15px 0; }
            .status { color: #00ff88; font-weight: bold; }
            .endpoint { background: #16213e; padding: 8px 15px; border-radius: 4px; font-family: monospace; margin: 5px 0; display: inline-block; }
            a { color: #00d4ff; }
        </style>
    </head>
    <body>
        <h1>DevOps Portfolio Dashboard</h1>

        <div class="card">
            <h2>Infrastructure Stack</h2>
            <ul>
                <li>Containerized with <strong>Docker</strong></li>
                <li>Infrastructure provisioned with <strong>Terraform</strong></li>
                <li>Orchestrated with <strong>Kubernetes</strong></li>
                <li>CI/CD via <strong>GitHub Actions</strong></li>
                <li>Monitored with <strong>Prometheus + Grafana</strong></li>
            </ul>
        </div>

        <div class="card">
            <h2>Endpoints</h2>
            <div class="endpoint">GET <a href="/health">/health</a> - Health check</div><br>
            <div class="endpoint">GET <a href="/metrics">/metrics</a> - Prometheus metrics</div><br>
            <div class="endpoint">GET <a href="/info">/info</a> - App info</div>
        </div>

        <div class="card">
            <h2>Status</h2>
            <p>Status: <span class="status">OPERATIONAL</span></p>
        </div>

        <div class="card">
            <h2>Links</h2>
            <ul>
                <li><a href="https://github.com/Kush999/devops-project">GitHub Repository</a></li>
                <li><a href="https://linkedin.com/in/YOUR_PROFILE">LinkedIn</a></li>
            </ul>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    # Increment our custom counter every time health is checked
    health_checks.inc()

    # Update CPU gauge with current value
    cpu_usage.set(psutil.cpu_percent())

    uptime = str(datetime.datetime.now() - START_TIME)
    return jsonify({
        "status": "healthy",
        "uptime": uptime,
        "timestamp": datetime.datetime.now().isoformat()
    }), 200

@app.route('/info')
def info():
    return jsonify({
        "app": "DevOps Portfolio Dashboard",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "deployed_by": "Terraform + GitHub Actions + Kubernetes"
    }), 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)