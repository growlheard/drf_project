from django.core.management.base import BaseCommand
from faker import Faker
import random
from users.models import User
from drf_app.models import Course, Lesson, Payment


class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми данными'

    def handle(self, *args, **kwargs):
        fake = Faker()

        for _ in range(10):
            name = fake.catch_phrase()
            image = None
            description = fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
            course = Course.objects.create(name=name, image=image, description=description)

            for _ in range(random.randint(3, 8)):
                lesson_name = fake.catch_phrase()
                lesson_description = fake.paragraph(nb_sentences=2, variable_nb_sentences=True)
                lesson_image = None
                lesson_video = fake.url()
                lesson = Lesson.objects.create(
                    name=lesson_name,
                    description=lesson_description,
                    image=lesson_image,
                    video=lesson_video,
                    course=course,
                )

        for _ in range(5):
            email = fake.email()
            phone = fake.phone_number()
            city = fake.city()
            avatar = None
            user = User.objects.create(email=email, phone=phone, city=city, avatar=avatar)

        for _ in range(10):  # Заполним 30 платежей
            user = random.choice(User.objects.all())
            date = fake.date_this_decade()
            lesson_pay = random.choice(Lesson.objects.all())
            course_pay = random.choice(Course.objects.all())
            amount = round(random.uniform(10, 1000), 2)
            payment_method = random.choice(['cash', 'transfer'])
            payment = Payment.objects.create(
                user=user,
                date=date,
                lesson_pay=lesson_pay,
                course_pay=course_pay,
                amount=amount,
                payment_method=payment_method,
            )

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно созданы!'))
