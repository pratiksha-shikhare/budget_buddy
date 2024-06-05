from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_task(subject, message, from_email, recipient_list):
    subject = 'Test Subject'
    message = 'This is a test message.'
    email_from = 'sender@example.com'
    recipient_list = ['recipient@example.com']
    send_mail(subject, message, email_from, recipient_list)

    # send_mail(subject, message, from_email, recipient_list)
