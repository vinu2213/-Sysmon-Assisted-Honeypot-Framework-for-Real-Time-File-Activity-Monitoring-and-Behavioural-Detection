# 🔐 Ransomware Detection System

## 📌 Overview
This project is a real-time ransomware detection system that monitors file activities using Sysmon and detects suspicious behavior using honeypot techniques and behavioral analysis.

## 🚀 Features
- Real-time file monitoring
- Honeypot-based detection
- Behavioral anomaly detection
- Alert system for suspicious activity
- Logging of file modifications

## 🛠 Technologies Used
- Python
- Watchdog
- Tkinter (GUI)
- Sysmon
- Machine Learning

## 📂 Project Structure
- app.py → Main application (GUI)
- detector.py → Detection logic
- honeypot.py → Honeypot file handling
- real_time_sysmon_detection.py → Sysmon integration
- dataset.csv → Training dataset

## ▶️ How to Run
```bash
pip install -r requirements.txt
python app.py
