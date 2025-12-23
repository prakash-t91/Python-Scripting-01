#!/usr/bin/env python3

import psutil
import shutil
import smtplib
import logging
import time
import sys
#import tqdm

#from tqdm import tqdm
from time import sleep
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ====== CONFIG SETTINGS ======
CPU_THRESHOLD = 80     # percent
MEMORY_THRESHOLD = 75  # percent
CHECK_INTERVAL = 10   # seconds = 5 minutes

EMAIL_FROM = "techprakashtp@gmail.com"
EMAIL_TO = "techprakashtp@gmail.com"
EMAIL_PASSWORD = "your_app_password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 25

LOG_FILE = "./server_monitor.log"

# ====== LOGGING SETUP ======
logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# ====== FUNCTION: Send Email ======
def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        logging.info("Email alert sent.")
    except Exception as e:
        logging.error(f"Email failed: {e}")

# ====== FUNCTION: Check System Health ======
def check_system_resources():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    total, used, free = shutil.disk_usage("/")

    print(f"CPU Usage: {cpu}%, Memory Usage: {memory}%")
    print(f"Disk Total: {total // (2**30)} GiB, Used: {used // (2**30)} GiB, Free: {free // (2**30)} GiB")

    logging.info(f"CPU: {cpu}%, Memory: {memory}%, Disk Free: {free // (2**30)} GiB")


    if cpu > CPU_THRESHOLD or memory > MEMORY_THRESHOLD:
        subject = "Server Alert: High Usage"
        body = (f" High resource usage detected!\n\n"
                f"CPU Usage: {cpu}% (Limit: {CPU_THRESHOLD}%)\n"
                f"Memory Usage: {memory}% (Limit: {MEMORY_THRESHOLD}%)")
        send_email(subject, body)

        #sleep(0.5)

# ====== LOOP: Run every 5 minutes ======
if __name__ == "__main__":
    logging.info("Monitoring started.")
    while True:
        check_system_resources()
        time.sleep(CHECK_INTERVAL)
sys.exit(0)