import smtplib
import subprocess
import sys
import os
import imaplib
import email
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# ========== User Configuration ==========
# Sender email account (your enterprise mailbox)
smtp_server = "smtp.exmail.qq.com"
smtp_port = 465
imap_server = "imap.exmail.qq.com"
sender_email = "your_email@example.com"
sender_password = os.getenv("EMAIL_PASS")  # Use environment variable for security
receiver_email = "your_email@example.com"
# ========== End Configuration ==========

def send_mail(subject, body, attachment_path=None):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
            part["Content-Disposition"] = f'attachment; filename="{os.path.basename(attachment_path)}"'
            msg.attach(part)

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Failed to send email:", e)

def run_command(command, log_file):
    print(f"🚀 Executing command: {command}")
    with open(log_file, "w") as log:
        process = subprocess.run(command, shell=True, stdout=log, stderr=subprocess.STDOUT)
    return process.returncode

def list_inbox(limit=10):
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(sender_email, sender_password)
        mail.select("inbox")

        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()

        print(f"📥 Latest {limit} email subjects:\n")
        for eid in email_ids[-limit:]:
            res, msg_data = mail.fetch(eid, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    print(f"✉️ Email ID: {eid.decode()} | Subject: {subject}")

        mail.logout()
    except Exception as e:
        print("❌ Failed to read inbox:", e)

def download_attachments(email_id, output_dir="."):
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(sender_email, sender_password)
        mail.select("inbox")

        status, msg_data = mail.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                for part in msg.walk():
                    if part.get_content_disposition() == "attachment":
                        filename = part.get_filename()
                        if filename:
                            decoded_name = decode_header(filename)[0][0]
                            if isinstance(decoded_name, bytes):
                                decoded_name = decoded_name.decode()
                            filepath = os.path.join(output_dir, decoded_name)
                            with open(filepath, "wb") as f:
                                f.write(part.get_payload(decode=True))
                            print(f"📎 Attachment saved: {filepath}")

        mail.logout()
    except Exception as e:
        print("❌ Failed to download attachments:", e)

def print_help():
    print("""
Usage:
  python run_with_mail_notify.py run "<command>" <log_file>         # Run command and send result via email
  python run_with_mail_notify.py send "<subject>" "<body>" <file>    # Manually send email with attachment
  python run_with_mail_notify.py inbox [count]                      # List recent email subjects
  python run_with_mail_notify.py download <email_id> [output_dir]   # Download attachments from specified email
  python run_with_mail_notify.py -h or --help                       # Show help message
""")

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print_help()
        sys.exit(0)

    mode = sys.argv[1]

    if mode == "run" and len(sys.argv) >= 4:
        command = sys.argv[2]
        logfile = sys.argv[3]
        retcode = run_command(command, logfile)
        subject = f"[Task Complete] Command executed (exit code: {retcode})"
        body = f"The command has been executed. Please see the attached log.\n\nCommand: {command}\nExit Code: {retcode}"
        send_mail(subject, body, logfile)

    elif mode == "send" and len(sys.argv) >= 5:
        subject = sys.argv[2]
        body = sys.argv[3]
        attachment = sys.argv[4]
        send_mail(subject, body, attachment)

    elif mode == "inbox":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        list_inbox(limit)

    elif mode == "download" and len(sys.argv) >= 3:
        email_id = sys.argv[2]
        outdir = sys.argv[3] if len(sys.argv) > 3 else "."
        download_attachments(email_id, outdir)

    else:
        print_help()
