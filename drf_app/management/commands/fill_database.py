from django.core.management.base import BaseCommand
from django.utils import timezone

from users.models import User
from drf_app.models import Course, Lesson, Payment, Subscription
from faker import Faker
from random import choice, randint

fake = Faker()

class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми данными'

    def handle(self, *args, **options):
        # Create users
        users = []
        for i in range(10):
            user = User.objects.create(
                email=fake.email(),
                password=fake.password(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=fake.phone_number(),
                city=fake.city(),
            )
            users.append(user)

        # Create courses
        courses = []
        for i in range(5):
            course = Course.objects.create(
                name=fake.sentence(),
                image=fake.image_url(width=640, height=480),
                description=fake.paragraph(),
                owner=choice(users),
                price=randint(500, 5000),
            )
            courses.append(course)

        # Create lessons
        for i in range(20):
            lesson = Lesson.objects.create(
                name=fake.sentence(),
                description=fake.paragraph(),
                image=fake.image_url(width=640, height=480),
                video=fake.url(),
                course=choice(courses),
                owner=choice(users),
            )

        # Create subscriptions
        for i in range(20):
            subscription = Subscription.objects.create(
                user=choice(users),
                course=choice(courses),
            )

        # Create payments
        for _ in range(20):
            user = choice(users)
            course = choice(courses)
            lesson_pay = choice(course.lesson_set.all()) if course.lesson_set.exists() else None
            amount = randint(500, 5000)
            payment_method = choice([
                Payment.PAYMENT_METHOD_CASH,
                Payment.PAYMENT_METHOD_TRANSFER,
            ])

            payment = Payment.objects.create(
                user=user,
                date=timezone.now(),
                lesson_pay=lesson_pay,
                course_pay=course,
                amount=amount,
                payment_method=payment_method,
                payment_intent_id=None,
                payment_method_id=None,
                status=None,
            )

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно созданы!'))