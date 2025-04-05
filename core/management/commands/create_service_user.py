from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates a service account for system integration'

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username=settings.SERVICE_ACCOUNT_USERNAME,
            defaults={
                'email': 'service@smartrazzakov.kg',
                'is_active': True,
                'is_service_account': True
            }
        )

        if created:
            user.set_unusable_password()
            user.save()
            self.stdout.write(self.style.SUCCESS('Service account created'))
        else:
            self.stdout.write(self.style.WARNING('Service account already exists'))