from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='manager@sky.pro',
            first_name='manager',
            last_name='manager',
            is_staff=True,
            is_superuser=False
        )

        user.set_password('manager')
        user.save()
