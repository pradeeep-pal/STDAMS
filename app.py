"""
app.py
Flask app for STDAMS API and dashboard.
"""
from flask import Flask, jsonify, render_template
import pandas as pd
import os
from model import detect_anomaly
from threat_engine import classify_threat

app = Flask(__name__)

DATA_FILE = 'data/satellite.csv'

# Helper to get latest telemetry
def get_latest_telemetry():
    if not os.path.exists(DATA_FILE):
        return None
    df = pd.read_csv(DATA_FILE)
    if df.empty:
        return None
    row = df.iloc[-1]
    return {
        'timestamp': row.get('timestamp', 'N/A'),
        'altitude': float(row['altitude']),
        'velocity': float(row['velocity']),
        'signal_strength': float(row['signal_strength']),
        'proximity_km': float(row.get('proximity_km', 100))
    }

# --- YEH ROUTE MISSING THA, ISE ADD KAREIN ---
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/telemetry')
def api_telemetry():
    telemetry = get_latest_telemetry()
    return jsonify(telemetry)

@app.route('/api/anomaly')
def api_anomaly():
    telemetry = get_latest_telemetry()
    if not telemetry:
        return jsonify({'status': 'NO DATA'})
    anomaly = detect_anomaly(telemetry)
    return jsonify(anomaly)

@app.route('/api/alerts')
def api_alerts():
    telemetry = get_latest_telemetry()
    if not telemetry:
        return jsonify({'level': 'NORMAL', 'message': 'No telemetry data.', 'type': 'None'})
    
    # ML model status (ANOMALY ya NORMAL)
    anomaly = detect_anomaly(telemetry) 
    
    # Threat Engine classification
    threat = classify_threat(telemetry, anomaly['status'])
    
    return jsonify({
        'level': threat['risk'],
        'message': threat['description'],
        'type': threat['type']
    })

if __name__ == '__main__':
    # Debug mode ON rakhein taaki errors dikhein
    app.run(debug=True, port=5000)