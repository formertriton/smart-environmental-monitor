from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import random
import json
from datetime import datetime

app = FastAPI(title="Environmental Monitor Demo")

@app.get("/")
async def dashboard():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Environmental Monitor</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body { font-family: Arial; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .card { background: white; padding: 20px; margin: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .metric { text-align: center; }
            .metric h2 { color: #333; margin: 0; }
            .metric .value { font-size: 3em; font-weight: bold; color: #2196F3; }
            .metric .unit { color: #666; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌍 Smart Environmental Monitor</h1>
            <div class="grid">
                <div class="card metric">
                    <h2>Temperature</h2>
                    <div class="value" id="temp">22.5</div>
                    <div class="unit">°C</div>
                </div>
                <div class="card metric">
                    <h2>Humidity</h2>
                    <div class="value" id="humidity">65</div>
                    <div class="unit">%</div>
                </div>
                <div class="card metric">
                    <h2>Air Quality</h2>
                    <div class="value" id="aqi">42</div>
                    <div class="unit">AQI</div>
                </div>
                <div class="card metric">
                    <h2>Pressure</h2>
                    <div class="value" id="pressure">1013</div>
                    <div class="unit">hPa</div>
                </div>
            </div>
            <div class="card">
                <canvas id="chart" width="400" height="200"></canvas>
            </div>
        </div>
        
        <script>
            // Simple real-time updates
            setInterval(() => {
                document.getElementById('temp').textContent = (20 + Math.random() * 10).toFixed(1);
                document.getElementById('humidity').textContent = Math.floor(50 + Math.random() * 30);
                document.getElementById('aqi').textContent = Math.floor(30 + Math.random() * 50);
                document.getElementById('pressure').textContent = Math.floor(1010 + Math.random() * 10);
            }, 2000);
            
            // Simple chart
            const ctx = document.getElementById('chart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['1h ago', '45m', '30m', '15m', 'Now'],
                    datasets: [{
                        label: 'Temperature',
                        data: [22, 23, 22.5, 24, 22.5],
                        borderColor: '#2196F3',
                        fill: false
                    }]
                }
            });
        </script>
    </body>
    </html>
    """)

@app.get("/api/data")
async def get_data():
    return {
        "timestamp": datetime.now().isoformat(),
        "sensors": {
            "temperature": round(20 + random.random() * 10, 1),
            "humidity": round(50 + random.random() * 30),
            "air_quality": round(30 + random.random() * 50),
            "pressure": round(1010 + random.random() * 10)
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Environmental Monitor Demo")
    print("📊 Dashboard: http://localhost:8000")
    print("🔌 API: http://localhost:8000/api/data")
    uvicorn.run(app, host="0.0.0.0", port=8000)