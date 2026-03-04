def classify_threat(telemetry, anomaly_status):
    # ML Status check (Sensitive check)
    # Agar model 'NORMAL' de raha hai tab bhi hum emergency thresholds check karenge
    is_emergency = telemetry['altitude'] < 490 or telemetry.get('signal_strength', 100) < 15

    if anomaly_status != 'ANOMALY' and not is_emergency:
        return {'type': 'None', 'risk': 'LOW', 'description': 'All systems nominal.'}

    # 1. ORBITAL DECAY (Altitude based)
    if telemetry['altitude'] < 380:
        return {
            'type': 'CRITICAL: Orbital Decay',
            'risk': 'CRITICAL', # Risk level matched with UI
            'description': f"Altitude critical: {telemetry['altitude']}km. Re-entry imminent!"
        }

    # 2. COLLISION RISK (Proximity based)
    # Ensure simulator is sending proximity_km
    prox = telemetry.get('proximity_km', 100) 
    if prox < 20: 
        return {
            'type': 'DANGER: Collision Imminent',
            'risk': 'CRITICAL',
            'description': f"Debris detected at {prox}km. Execute maneuver!"
        }

    # 3. SIGNAL/CYBER (Signal strength based)
    sig = telemetry.get('signal_strength', 100)
    if sig < 25:
        return {
            'type': 'SECURITY: Signal Jamming',
            'risk': 'WARNING', # WARNING class in your CSS
            'description': f"Signal strength dropped to {sig}%. Interference detected."
        }

    # 4. KINETIC (Velocity based)
    # Adjust 7.5 to your simulator's average velocity
    current_vel = telemetry['velocity']
    if abs(current_vel - 7.5) > 1.0:
        return {
            'type': 'PHYSICAL: Velocity Anomaly',
            'risk': 'WARNING',
            'description': f"Unstable velocity: {current_vel} km/s."
        }

    return {'type': 'SYSTEM: Unknown Anomaly', 'risk': 'WARNING', 'description': 'Irregular pattern detected.'}