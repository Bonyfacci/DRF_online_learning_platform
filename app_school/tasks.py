from celery import shared_task
from django.core.mail import send_mail

from config import settings


@shared_task
def send_mail_about_update(user_email, course_title):
    print(f'Материалы курса {course_title} обновились!')
    send_mail(
        subject=f'Обновление курса {course_title}',
        message=f'Материалы курса {course_title} обновились!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
    )
