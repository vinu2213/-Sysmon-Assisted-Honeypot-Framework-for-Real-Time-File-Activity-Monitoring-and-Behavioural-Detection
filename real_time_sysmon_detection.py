import win32evtlog
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import time
import joblib
import re

# --------------------------------------------
# STEP 1: Load pre-trained ML model or dataset
# --------------------------------------------
df = pd.read_csv("sysmon_honeypot_dataset_500.csv")
features = ['Entropy','FileAccessCount','ModificationCount','AccessInterval']
X = df[features]
y = df['Label']

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

print("✅ Model loaded and ready for real-time detection.\n")

# --------------------------------------------
# STEP 2: Connect to Sysmon Event Log
# --------------------------------------------
server = 'localhost'
log_type = 'Microsoft-Windows-Sysmon/Operational'
hand = win32evtlog.OpenEventLog(server, log_type)

flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

# --------------------------------------------
# STEP 3: Monitor Logs in Real-Time
# --------------------------------------------
print("🔍 Monitoring live Sysmon logs...\n(Press Ctrl+C to stop)\n")

seen_records = set()
alert_count = 0

while True:
    events = win32evtlog.ReadEventLog(hand, win32evtlog.EVENTLOG_SEQUENTIAL_READ | win32evtlog.EVENTLOG_FORWARDS_READ, 0)
    if not events:
        time.sleep(1)
        continue

    for ev_obj in events:
        try:
            record_id = ev_obj.RecordNumber
            if record_id in seen_records:
                continue
            seen_records.add(record_id)

            # Extract basic event data
            event_id = ev_obj.EventID
            msg = ev_obj.StringInserts

            if event_id == 11:  # FileCreate
                file_path = msg[3] if len(msg) > 3 else ""
                proc_name = msg[0] if len(msg) > 0 else ""
                
                # Simulate feature extraction
                entropy = 7.8 if "honeypot" in file_path.lower() else 3.0
                access_count = 10 if "honeypot" in file_path.lower() else 2
                modification = 8 if "honeypot" in file_path.lower() else 1
                interval = 0.2 if "honeypot" in file_path.lower() else 3.5

                # ML prediction
                X_input = pd.DataFrame([[entropy, access_count, modification, interval]], columns=features)
                pred = model.predict(X_input)[0]
                prob = model.predict_proba(X_input)[0, 1]

                if pred == 1:
                    alert_count += 1
                    print(f"🚨 ALERT #{alert_count} | Suspicious file activity detected!")
                    print(f"File: {file_path}\nProcess: {proc_name}\nMalicious Probability: {prob:.3f}\n")
                    with open("alerts.log", "a") as f:
                        f.write(f"{time.ctime()} ALERT - File={file_path} Prob={prob:.3f}\n")

        except Exception as e:
            continue

    time.sleep(2)
