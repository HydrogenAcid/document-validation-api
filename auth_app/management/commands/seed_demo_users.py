from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create demo users for the technical test (idempotent)."

    def handle(self, *args, **options):
        User = get_user_model()

        users = [
            {"username": "demo", "password": "demo12345", "email": "demo@example.com"},
            {"username": "demo2", "password": "demo212345", "email": "demo2@example.com"},
        ]

        for u in users:
            obj, created = User.objects.get_or_create(
                username=u["username"],
                defaults={"email": u["email"]},
            )
            obj.set_password(u["password"])
            if not obj.email:
                obj.email = u["email"]
            obj.save()

            self.stdout.write(
                self.style.SUCCESS(f"{'Created' if created else 'Updated'} user: {u['username']}")
            )