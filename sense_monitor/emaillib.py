import smtplib
from sense_monitor.secret import GMAIL_PASSWORD, PHONE_EMAIL_ADDR

# Email Variables
SMTP_SERVER = 'smtp.gmail.com'  # Email Server (don't change!)
SMTP_PORT = 587  # Server Port (don't change!)
GMAIL_USERNAME = 'genericcarbonlifeform@gmail.com'  # change this to match your gmail account


def send_email(send_to, subject, body):
    headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + send_to,
               "MIME-Version: 1.0", 'Content-Type: text/plain; charset="UTF-8"']
    headers = "\r\n".join(headers)
    msg = headers + "\r\n\r\n" + body

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as session:
        session.ehlo()
        session.starttls()
        session.ehlo()

        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
        session.sendmail(GMAIL_USERNAME, send_to, msg)

if __name__ == '__main__':
    send_email(
        send_to=PHONE_EMAIL_ADDR,
        #send_to="GenericLifeform@gmail.com",
        subject="Testing6",
        body=""
    )
