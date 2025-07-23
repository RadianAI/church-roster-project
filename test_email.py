import smtplib
from email.message import EmailMessage

def send_test_email():
    msg = EmailMessage()
    msg["From"] = "braydenjo@gmail.com"  # put your Gmail address here
    msg["To"] = "braydenjo@gmail.com"    # send the test email to yourself
    msg["Subject"] = "Test Email from Python"
    msg.set_content("Hello Brayden! This is a test email from your Python script.")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("braydenjo@gmail.com", "xrtdrgxtptnsmpqd")  # your App Password here, no spaces
        smtp.send_message(msg)
        print("Email sent!")

if __name__ == "__main__":
    send_test_email()
