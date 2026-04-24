import tkinter as tk
from tkinter import scrolledtext
import subprocess
import os
import honeypot

process = None
threat_count = 0

def start_detection():
    global process
    if process is None:
        process = subprocess.Popen(["python", "detector.py"])
        status_label.config(text="Status: Monitoring")

def stop_detection():
    global process
    if process:
        process.terminate()
        process = None
        status_label.config(text="Status: Stopped")

def create_honeypot_files():
    msg = honeypot.create_honeypot()
    log_display.insert(tk.END, msg + "\n")

def open_logs():
    log_path = os.path.join("logs", "alerts.log")
    if os.path.exists(log_path):
        os.startfile(log_path)

def update_logs():
    global threat_count

    try:
        log_path = "logs/alerts.log"
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                content = f.read()

                log_display.delete(1.0, tk.END)
                log_display.insert(tk.END, content)

                threat_count = content.count("ALERT")
                threat_label.config(text=f"Threats Detected: {threat_count}")

    except:
        pass

    root.after(2000, update_logs)

# GUI
root = tk.Tk()
root.title("Ransomware Detection Tool")
root.geometry("420x500")

title = tk.Label(root, text="Sysmon Honeypot Detector", font=("Arial", 14))
title.pack(pady=10)

status_label = tk.Label(root, text="Status: Idle")
status_label.pack()

threat_label = tk.Label(root, text="Threats Detected: 0")
threat_label.pack()

tk.Button(root, text="Start Monitoring", command=start_detection).pack(pady=5)
tk.Button(root, text="Stop Monitoring", command=stop_detection).pack(pady=5)
tk.Button(root, text="Create Honeypot Files", command=create_honeypot_files).pack(pady=5)
tk.Button(root, text="View Logs", command=open_logs).pack(pady=5)

log_display = scrolledtext.ScrolledText(root, height=15, width=50)
log_display.pack(pady=10)

update_logs()

root.mainloop()