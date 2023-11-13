from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from app import settings

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username = 'admin'
            email = 'admin@admin.com'
            password = 'admin'
            print('Creating account for %s (%s)' % (username, email))
            admin = User.objects.create_superuser(email=email, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')