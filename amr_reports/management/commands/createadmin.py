from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os
import sys

class Command(BaseCommand):
    help = 'Create or update admin user from env vars. Env vars: DJANGO_ADMIN_USERNAME, DJANGO_ADMIN_PASSWORD, DJANGO_ADMIN_EMAIL'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DJANGO_ADMIN_USERNAME')
        password = os.environ.get('DJANGO_ADMIN_PASSWORD')
        email = os.environ.get('DJANGO_ADMIN_EMAIL', 'admin@example.com')

        if not username or not password:
            self.stdout.write(self.style.WARNING('DJANGO_ADMIN_USERNAME and DJANGO_ADMIN_PASSWORD not set — skipping admin creation/password update.'))
            return

        try:
            user = User.objects.filter(username=username).first()
            if user:
                # Update password if different
                if not user.check_password(password):
                    user.set_password(password)
                    if email:
                        user.email = email
                    user.is_staff = True
                    user.is_superuser = True
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f'Updated password for existing admin user \"{username}\".'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Admin user \"{username}\" already exists with the same password.'))
                return

            # create if not exists
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Created admin user \"{username}\".'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to create/update admin user: {e}'))
            print(file=sys.stderr)
            import traceback; traceback.print_exc()
            sys.exit(1)
