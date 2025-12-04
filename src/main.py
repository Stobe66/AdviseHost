#!/usr/bin/env python3
import os
import sys
import logging
from datetime import datetime, timedelta
import pytz
from icalevents.icalevents import events
from email.message import EmailMessage
import smtplib

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def get_env(name, default=None, required=False):
    v = os.getenv(name, default)
    if required and (v is None or v == ""):
        logging.error("Environment variable %s is required", name)
        sys.exit(2)
    return v

def fetch_events(ical_url, start, end):
    logging.info("Fetching events from %s between %s and %s", ical_url, start.isoformat(), end.isoformat())
    try:
        evs = events(url=ical_url, start=start, end=end)
        return evs
    except Exception as e:
        logging.exception("Failed to fetch or parse iCal: %s", e)
        return []

def format_events(evs, timezone):
    lines = []
    for e in sorted(evs, key=lambda x: x.start):
        start_local = e.start.astimezone(timezone)
        end_local = e.end.astimezone(timezone) if e.end else None
        timestr = start_local.strftime("%Y-%m-%d %H:%M")
        if end_local:
            timestr += " - " + end_local.strftime("%H:%M")
        summary = getattr(e, "summary", "") or ""
        location = getattr(e, "location", "") or ""
        desc = getattr(e, "description", "") or ""
        lines.append(f"- {timestr} | {summary} | {location}\n  {desc}")
    return "\n".join(lines) if lines else "Ei tapahtumia."

def send_email(smtp_host, smtp_port, smtp_user, smtp_pass, email_from, email_to, subject, body):
    msg = EmailMessage()
    msg["From"] = email_from
    msg["To"] = email_to
    msg["Subject"] = subject
    msg.set_content(body)

    logging.info("Sending email to %s via %s:%s", email_to, smtp_host, smtp_port)
    try:
        smtp_port = int(smtp_port)
        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as s:
            s.starttls()
            s.login(smtp_user, smtp_pass)
            s.send_message(msg)
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.exception("Failed to send email: %s", e)
        sys.exit(3)

def main():
    ical_url = get_env("ICAL_URL", required=True)
    smtp_host = get_env("SMTP_HOST", required=True)
    smtp_port = get_env("SMTP_PORT", required=True)
    smtp_user = get_env("SMTP_USER", required=True)
    smtp_pass = get_env("SMTP_PASS", required=True)
    email_from = get_env("EMAIL_FROM", required=True)
    email_to = get_env("EMAIL_TO", required=True)
    days_ahead = int(get_env("DAYS_AHEAD", "2"))
    tz_name = get_env("TZ", "UTC")

    try:
        tz = pytz.timezone(tz_name)
    except Exception:
        logging.warning("Invalid TZ '%s', falling back to UTC", tz_name)
        tz = pytz.UTC

    now = datetime.now(tz)
    start = now
    end = now + timedelta(days=days_ahead)

    evs = fetch_events(ical_url, start, end)
    body_header = f"Kalenterikooste: seuraavat {days_ahead} päivää ({start.date()} - {end.date()})\n\n"
    body_events = format_events(evs, tz)
    body = body_header + body_events

    subject = f"Kalenterikooste: seuraavat {days_ahead} päivää"
    send_email(smtp_host, smtp_port, smtp_user, smtp_pass, email_from, email_to, subject, body)

if __name__ == "__main__":
    main()