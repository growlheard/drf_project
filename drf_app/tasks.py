from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime, timedelta
from config import settings
from drf_app.models import Course, Subscription
from users.models import User


@shared_task
def send_update_email(course_id):
    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(course=course, status=True)

        if course.last_update < timezone.now() - timedelta(hours=4):
            for subscription in subscriptions:
                user = subscription.user
                send_mail(
                    f'Курс {course.name} был обновлен. Проверьте новый материал!',
                    'Обновление',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
    except Course.DoesNotExist:
        print('Нет подписчиков на этот курс')


@shared_task
def check_active_user():
    now_date = datetime.now()
    one_month_ago = now_date - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago)
    inactive_users.update(is_active=False)
    print('Пользователь теперь неактивен')
