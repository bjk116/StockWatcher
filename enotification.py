"""
For emailing me alerts.
"""
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import json

def sendEmail(message):
    subject = message['title']
    body = message['subtitle']
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    user = None
    password = None
    with open('config.json', 'r') as f:
        data = json.load(f)['email']
        user = data['user']
        password = data['password']
    smtp.ehlo()
    smtp.starttls()
    print(f"Logging in with {user}, {password}")
    smtp.login(user, password)
    msg = MIMEMultipart()
    msg['subject'] = subject
    msg.attach(MIMEText(body))
    to=['karabinchak.brian@gmail.com']
    print(f"About to send email from {data['user']} to {to}")
    smtp.sendmail(from_addr=data['user'], to_addrs=to, msg=msg.as_string())
    smtp.quit()

if __name__ == "__main__":
    sendEmail()
