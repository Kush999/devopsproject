from flask import Flask, jsonify
import psutil
import datetime
import os

app = Flask(__name__)

# Track when the app started
START_TIME = datetime.datetime.now()

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>DevOps Portfolio - Kush Dhuvad</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: 50px auto;
                padding: 20px;
                background-color: #0a0a0a;
                color: #e0e0e0;
            }
            h1 {
                color: #00d4ff;
                border-bottom: 2px solid #00d4ff;
                padding-bottom: 10px;
            }
            h2 {
                color: #00d4ff;
            }
            .card {
                background: #1a1a2e;
                border: 1px solid #16213e;
                border-radius: 8px;
                padding: 20px;
                margin: 15px 0;
            }
            .status {
                color: #00ff88;
                font-weight: bold;
            }
            .endpoint {
                background: #16213e;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: monospace;
                margin: 5px 0;
                display: inline-block;
            }
            a {
                color: #00d4ff;
            }
        </style>
    </head>
    <body>
        <h1>DevOps Portfolio Dashboard</h1>
        <p>Built and deployed by <strong>Kush Dhuvad</strong></p>

        <div class="card">
            <h2>About This Project</h2>
            <p>This application is deployed using a complete 
               DevOps pipeline:</p>
            <ul>
                <li>Containerized with <strong>Docker</strong></li>
                <li>Infrastructure provisioned with 
                    <strong>Terraform</strong></li>
                <li>CI/CD via <strong>GitHub Actions</strong></li>
                <li>Monitored with <strong>Prometheus + 
                    Grafana</strong></li>
            </ul>
        </div>

        <div class="card">
            <h2>Live API Endpoints</h2>
            <p>These endpoints are actively monitored:</p>
            <div class="endpoint">
                GET <a href="/health">/health</a> 
                - Health check
            </div><br>
            <div class="endpoint">
                GET <a href="/metrics">/metrics</a> 
                - System metrics
            </div><br>
            <div class="endpoint">
                GET <a href="/info">/info</a> 
                - App information
            </div>
        </div>

        <div class="card">
            <h2>System Status</h2>
            <p>Status: <span class="status">OPERATIONAL v2.0 - Deployed via CI/CD 🚀</span></p>
            <p>Check <a href="/health">/health</a> 
               for real-time status</p>
        </div>

        <div class="card">
            <h2>Links</h2>
            <ul>
                <li><a href="https://github.com/kushdhuvad/devops-project">
                    GitHub Repository</a></li>
                <li><a href="https://linkedin.com/in/kushdhuvad">
                    LinkedIn</a></li>
            </ul>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    """Health check endpoint - used by monitoring systems"""
    uptime = str(datetime.datetime.now() - START_TIME)
    return jsonify({
        "status": "healthy",
        "uptime": uptime,
        "timestamp": datetime.datetime.now().isoformat()
    }), 200

@app.route('/metrics')
def metrics():
    """System metrics endpoint - used by Prometheus later"""
    return jsonify({
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent
    }), 200

@app.route('/info')
def info():
    """App info endpoint"""
    return jsonify({
        "app": "DevOps Portfolio Dashboard",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "deployed_by": "Terraform + GitHub Actions"
    }), 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)