import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.header import Header
import random


def send_ya_mail(recipients_emails: list, msg_text: str):
    load_dotenv()
    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD') 
    msg = MIMEText(f'{msg_text}', 'plain', 'utf-8')
    msg['Subject'] = Header('Подтверждение почты', 'utf-8')
    msg['From'] = login
    msg['To'] = ', '.join(recipients_emails)

    s = smtplib.SMTP('smtp.yandex.ru', 587, timeout=10)

    try:
        s.starttls()
        s.login(login, password)
        s.sendmail(msg['From'], recipients_emails, msg.as_string())
    except Exception as ex:
        print(ex)
    finally:
        s.quit()