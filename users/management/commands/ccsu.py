from django.core.management import BaseCommand

from users.models import User, UserRoles

class Command(BaseCommand):

    def handle(self, *args, **options):
        admin = User.objects.create(
            email='admin@web.top',
            first_name='Admin',
            last_name='Adminov',
            role=UserRoles.ADMIN,
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        admin.set_password('qwerty')
        admin.save()
        print('Admin Created')

        moderator = User.objects.create(
            email='moderator@web.top',
            first_name='Moderator',
            last_name='Moderatov',
            role=UserRoles.MODERATOR,
            is_staff=True,
            is_superuser=False,
            is_active=True
        )

        moderator.set_password('qwerty')
        moderator.save()
        print('Moderator Created')

        user = User.objects.create(
            email='user@web.top',
            first_name='User',
            last_name='Userov',
            role=UserRoles.USER,
            is_staff=True,
            is_superuser=False,
            is_active=True
        )

        user.set_password('qwerty')
        user.save()
        print('User Created')