import time
import os
import smtplib
import ctypes
from email.mime.text import MIMEText
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tkinter as tk
from tkinter import messagebox

modification_times = []
PATHS_TO_MONITOR = [
    os.path.join(os.environ["USERPROFILE"], "Desktop"),
    os.path.join(os.environ["USERPROFILE"], "Documents"),
    os.path.join(os.environ["USERPROFILE"], "Downloads")
]
class HoneypotHandler(FileSystemEventHandler):

    def log_alert(self, message):
        os.makedirs("logs", exist_ok=True)
        log_path = os.path.join("logs", "alerts.log")

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(message + "\n")

        print(message)

    import ctypes

    def show_popup(self, message):
     ctypes.windll.user32.MessageBoxW(0, message, "Ransomware Alert!", 1)

    def send_email(self, message):
      sender = "your_email@gmail.com"
      receiver = "your_email@gmail.com"
      password = "ulsdyedtwnkvggrh"

      msg = MIMEText(message)
      msg["Subject"] =  "🚨 Ransomware Alert Detected!"
      msg["From"] = sender
      msg["To"] = receiver

      try:
         server = smtplib.SMTP("smtp.gmail.com", 587)
         server.starttls()
         server.login(sender, password)
         server.send_message(msg)
         server.quit()
         print("Email sent successfully")
      except Exception as e:
         print("Email failed:", e)

    def on_modified(self, event):
      global modification_times

      if not event.is_directory:
        file_name = os.path.basename(event.src_path)

        # Ignore log file
        if "alerts.log" in event.src_path:
            return

        # Filter important files only
        if not file_name.endswith((".txt", ".docx", ".pdf", ".xlsx")):
            return

        current_time = time.time()
        modification_times.append(current_time)

        modification_times = [t for t in modification_times if current_time - t < 10]

        if len(modification_times) > 5:
            msg = "RANSOMWARE ALERT: Multiple rapid modifications detected!"
            self.log_alert(msg)
            self.show_popup(msg)

        alert = f"ALERT: File modified -> {file_name}"
        self.log_alert(alert)

    def on_created(self, event):
        name = os.path.basename(event.src_path)
        alert = f"ALERT: New file/folder created -> {name}"
        self.log_alert(alert)

    def on_deleted(self, event):
        name = os.path.basename(event.src_path)
        alert = f"ALERT: File/folder deleted -> {name}"
        self.log_alert(alert)


def start_monitoring():
    event_handler = HoneypotHandler()
    observer = Observer()

    for path in PATHS_TO_MONITOR:
        if os.path.exists(path):
            print(f"Monitoring: {path}")
            observer.schedule(event_handler, path, recursive=True)
        else:
            print(f"Path not found: {path}")

    observer.start()

    print("Monitoring system folders...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    start_monitoring()