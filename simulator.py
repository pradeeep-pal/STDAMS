import time
import random
import csv
import os
from datetime import datetime

DATA_FILE = 'data/satellite.csv'

# Normal values
ALTITUDE = 420.0
VELOCITY = 7.6
SIGNAL = 98.0
PROXIMITY = 100.0 # New field for Collision Detection

def generate_telemetry():
    global ALTITUDE, VELOCITY, SIGNAL, PROXIMITY
    
    # 1. Normal Random Drift
    ALTITUDE += random.uniform(-2.0, 2.0)
    VELOCITY += random.uniform(-0.02, 0.02)
    SIGNAL += random.uniform(-0.3, 0.3)
    PROXIMITY += random.uniform(-2.0, 2.0)

    # 2. Inject Anomaly (20% chance for more action)
    if random.random() < 0.20:
        event = random.choice(['drop', 'jam', 'close'])
        if event == 'drop':
            ALTITUDE -= random.uniform(5, 10) # Orbital decay test
        elif event == 'jam':
            SIGNAL -= random.uniform(15, 30) # Cyber attack test
        elif event == 'close':
            PROXIMITY = random.uniform(5, 18) # Collision test

    # 3. Clamping (Scale ke andar rakhein)
    ALTITUDE = max(345, min(ALTITUDE, 455)) # Dashboard scale: 340-460
    VELOCITY = max(7.1, min(VELOCITY, 8.4)) 
    SIGNAL = max(10, min(SIGNAL, 100))
    PROXIMITY = max(5, min(PROXIMITY, 150))

    return {
        'timestamp': datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + 'Z',
        'altitude': round(ALTITUDE, 2),
        'velocity': round(VELOCITY, 2),
        'signal_strength': round(SIGNAL, 2),
        'proximity_km': round(PROXIMITY, 2)
    }

def write_telemetry(row):
    file_exists = os.path.isfile(DATA_FILE)
    with open(DATA_FILE, 'a', newline='') as f:
        # Fieldnames updated with proximity_km
        fieldnames = ['timestamp', 'altitude', 'velocity', 'signal_strength', 'proximity_km']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

if __name__ == '__main__':
    # File saaf karke start karein taaki purana junk data na ho
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
        
    print('Starting STDAMS Telemetry Simulator...')
    while True:
        data = generate_telemetry()
        write_telemetry(data)
        print(f"Data Sent: Alt: {data['altitude']} | Signal: {data['signal_strength']} | Prox: {data['proximity_km']}")
        time.sleep(2) # Refresh rate fast