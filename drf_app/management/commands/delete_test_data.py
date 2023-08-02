from django.core.management.base import BaseCommand
from drf_app.models import Course, Lesson, Payment, User


class Command(BaseCommand):
    help = 'Удаление тестовых данных из базы данных'

    def handle(self, *args, **kwargs):
        # Удаление всех платежей
        Payment.objects.all().delete()

        # Удаление всех уроков
        Lesson.objects.all().delete()

        # Удаление всех курсов
        Course.objects.all().delete()

        # Удаление всех пользователей
        User.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно удалены!'))
