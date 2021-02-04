import smtplib
from sense_monitor.secret import GMAIL_PASSWORD

# Email Variables
SMTP_SERVER = 'smtp.gmail.com'  # Email Server (don't change!)
SMTP_PORT = 587  # Server Port (don't change!)
GMAIL_USERNAME = 'genericcarbonlifeform@gmail.com'  # change this to match your gmail account


def send_email(send_to, subject, body):
    # Create Headers
    headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + send_to,
               "MIME-Version: 1.0", "Content-Type: text/html"]
    headers = "\r\n".join(headers)

    # Connect to Gmail Server
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()

    # Login to Gmail
    session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

    # Send Email & Exit
    session.sendmail(GMAIL_USERNAME, send_to, headers + "\r\n\r\n" + body)
    session.quit()

if __name__ == '__main__':
    send_email(
        send_to="genericlifeform@gmail.com",
        subject="Testing",
        body="This is the body"
    )
