from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@gmail.com',
            first_name='Admin',
            last_name='Gmail',
            is_staff=True,
            is_superuser=True

        )

        user.set_password('qwerty')
        user.save()