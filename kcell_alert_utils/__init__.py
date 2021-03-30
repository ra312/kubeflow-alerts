from kfp import dsl

import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

def send_email(sender, recipient, text=''):
    try:
        sender = 'rauan.akylzhanov@kcell.kz'
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = "Hello from Kubeflow"
        msg.attach(MIMEText(text, 'plain'))

        server = smtplib.SMTP('smtp1.kcell.kz', 25)
        recipients = [recipient]
        server.sendmail(sender, [recipient], msg.as_string())
        print(f'Sent to {recipient}')
    except Exception as err:
        print("errors send email:", err)

import os
sender = os.environ['SENDER']
recipient = os.environ['RECIPIENT']
text = os.environ['TEXT']

send_email(sender=sender, recipient=recipient, text=text)
