# CLI Mail Assistant

A lightweight Python-based command-line tool to run shell commands, send result logs via email, check inbox content, and download attachments from specific emails. Perfect for researchers and server-based task automation.

## 📌 Features

- ✅ Automatically run a command and send result logs via email
- ✅ Manually send email with attachment
- ✅ List recent emails with subject and ID
- ✅ Download attachments from a specific email
- ✅ CLI-friendly with `-h` help

## 🔧 Usage

```bash
# Run a shell command and send notification email
python run_with_mail_notify.py run "command" result.log

# Send a custom email with attachment
python run_with_mail_notify.py send "Subject" "Body text" result.log

# View latest 5 email subjects
python run_with_mail_notify.py inbox 5

# Download attachments from email with ID 1234
python run_with_mail_notify.py download 1234 ./attachments

# Show usage help
python run_with_mail_notify.py -h
```

## 🔐 Mail Configuration
### You should also configure the following parameters in the script
```bash
# Sender email account (your enterprise mailbox)
smtp_server = "smtp.exmail.qq.com"           # SMTP server for sending emails
smtp_port = 465                              # SMTP SSL port
imap_server = "imap.exmail.qq.com"           # IMAP server for reading inbox
sender_email = "your_email@example.com"      # Your email address
sender_password = os.getenv("EMAIL_PASS")    # Read password from environment variable
receiver_email = "your_email@example.com"    # Recipient email address
```

### 📌 Set your email authorization token via environment variable
```bash
export EMAIL_PASS="your_email_authorization_code"
```
