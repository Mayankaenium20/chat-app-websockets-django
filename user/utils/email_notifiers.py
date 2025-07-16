from django.core.mail import send_mail
from django.conf import settings


def send_otp_email(to_email, otp):
    subject = "your otp for password change!"
    message = f"your otp is {otp}."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])