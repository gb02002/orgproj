import smtplib
from email.message import EmailMessage
from datetime import datetime
from celery import Celery, shared_task
from django.contrib.auth.models import User

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = ''
SMTP_PASSWORD = ''

celery = Celery('tasks', broker='redis://localhost:6379')


def news_email_template(user: User):
    email = EmailMessage()
    email['Subject'] = 'Test News'
    email['From'] = SMTP_USER
    email['To'] = user.email

    email.set_content(
        '<div>'
        f'<h2>Hello {user.username},</h2>'
        '<p>This is a news update email template.</p>'
        '<p>Here are some important news updates:</p>'
        '<ul>'
        '<li>News 1: Lorem ipsum dolor sit amet, consectetur adipiscing elit.</li>'
        '<li>News 2: Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</li>'
        '<li>News 3: Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo '
        'consequat.</li>'
        '</ul>'
        '<p>Thank you for your attention.</p>'
        '<p>Sincerely,</p>'
        '<p>Your Organization</p>'
        '</div>'
    )

    return email


def new_agent_email(user: User):
    email = EmailMessage()
    email['Subject'] = 'New Agent'
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    email.set_content(
        '<div>'
        f'<h2>Hello, there are new agent registered: {user.username} </h2>'
        '<ul>'
        f'<li>Name:{user.first_name} {user.last_name}</li>'
        f'<li>Email:{user.email}</li>'
        f'<li>Time joined: {user.date_joined}</li>'
        f'<li>Time: {current_time}</li>'
        '</ul>'
        '<p>One more day</p>'
        '<p>Sincerely,</p>'
        '<p>You</p>'
        '</div>'
    )

    return email


def today_logs_email(e):
    email = EmailMessage()
    email['Subject'] = "Today's logs"
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    email.set_content(
        '<div>'
        f'<h2>Hello, there are logs for {current_time}</h2>'  # Вставляем время в заголовок
        '<ul>'
        "We've got wierd stuff going here, unhandable and unexpecting:" 
        f"{e}"
        '</ul>'
        '<p>One more day</p>'
        '<p>Sincerely,</p>'
        '<p>You</p>'
        '</div>'
    )

    return email


def alert_errors_email():
    email = EmailMessage()
    email['Subject'] = "Critical error"
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    email.set_content(
        '<div>'
        f'<h2>Houston, we have a problem</h2>'  # Вставляем время в заголовок
        f'<h4>It was error:</h4>'  # Вставляем время в заголовок
        f'<h4>time {current_time}</h4>'  # Вставляем время в заголовок
        '<ul>'

        '</ul>'
        '<p>One more day</p>'
        '<p>Sincerely,</p>'
        '<p>You</p>'
        '</div>'
    )

    return email


@celery.task
def send_news(user: User):
    email = news_email_template(user)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)


@celery.task
def send_mail_new_agent(user: User):
    email = new_agent_email(user)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)


@celery.task
def send_todays_stats():
    """Collecting stats"""
    pass


@celery.task
def send_todays_logs():
    email = today_logs_email()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)


@celery.task
def alert_error_mail(e):
    email = today_logs_email(e)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
