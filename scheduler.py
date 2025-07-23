from datetime import datetime, timedelta
import threading
import schedule
import time
import smtplib
from email.message import EmailMessage

_scheduler_thread = None
_scheduler_running = False
_rows = []

def send_email(to_email, subject, body, email_user, email_pass):
    msg = EmailMessage()
    msg["From"] = email_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_user, email_pass)
        smtp.send_message(msg)
        print(f"Sent email to {to_email}")

def check_and_send_reminders(rows, email_user, email_pass):
    today = datetime.now().date()
    for row in rows:
        try:
            duty_date = datetime.strptime(row["date"], "%B %d").replace(year=today.year).date()
        except ValueError:
            print(f"Skipping invalid date: {row['date']}")
            continue

        days_before = (duty_date - today).days
        if days_before not in [7, 1]:
            continue

        # I.T. Operator email
        it_email = row.get("it_email", "").strip()
        it_name = row.get("it", "").strip()
        if it_email:
            subject = f"Church Duty Reminder: {duty_date.strftime('%B %d, %Y')}"
            body = f"Hey {it_name},\nOn {duty_date.strftime('%B %d, %Y')}, you are on I.T. Operator."
            send_email(it_email, subject, body, email_user, email_pass)

        # P.A. Operator email
        pa_email = row.get("pa_email", "").strip()
        pa_name = row.get("pa", "").strip()
        if pa_email:
            subject = f"Church Duty Reminder: {duty_date.strftime('%B %d, %Y')}"
            body = f"Hey {pa_name},\nOn {duty_date.strftime('%B %d, %Y')}, you are on P.A. Operator."
            send_email(pa_email, subject, body, email_user, email_pass)

def job(rows, email_user, email_pass):
    check_and_send_reminders(rows, email_user, email_pass)

def scheduler_loop(rows, email_user, email_pass):
    global _scheduler_running
    _scheduler_running = True
    schedule.clear()
    schedule.every().day.at("09:00").do(job, rows=rows, email_user=email_user, email_pass=email_pass)

    while _scheduler_running:
        schedule.run_pending()
        time.sleep(60)

def start_scheduler(filepath, email_user, email_pass):
    global _scheduler_thread, _rows
    from app import parse_roster
    _rows = parse_roster(filepath)

    if _scheduler_thread and _scheduler_thread.is_alive():
        # Scheduler already running
        return

    _scheduler_thread = threading.Thread(target=scheduler_loop, args=(_rows, email_user, email_pass), daemon=True)
    _scheduler_thread.start()
    print("Scheduler started.")

def stop_scheduler():
    global _scheduler_running
    _scheduler_running = False

def is_scheduler_running():
    return _scheduler_running

def get_rows():
    return _rows
