from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os
import sys

class Command(BaseCommand):
    help = 'Create admin user from env vars if not exists. Environment variables: DJANGO_ADMIN_USERNAME, DJANGO_ADMIN_PASSWORD, DJANGO_ADMIN_EMAIL'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DJANGO_ADMIN_USERNAME')
        password = os.environ.get('DJANGO_ADMIN_PASSWORD')
        email = os.environ.get('DJANGO_ADMIN_EMAIL', 'admin@example.com')

        if not username or not password:
            self.stdout.write(self.style.WARNING('DJANGO_ADMIN_USERNAME and DJANGO_ADMIN_PASSWORD not set — skipping admin creation.'))
            return

        try:
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.SUCCESS(f'Admin user \"{username}\" already exists.'))
                return

            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Created admin user \"{username}\".'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to create admin user: {e}'))
            # Print full exception on Render logs for debugging
            print(file=sys.stderr)
            import traceback; traceback.print_exc()
