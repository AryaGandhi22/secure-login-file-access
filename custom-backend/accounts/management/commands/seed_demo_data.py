from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from files.models import UserFile
from django.core.files.base import ContentFile


DEMO_USERS = [
    {
        "email": "alice@example.com",
        "password": "Password123!",
        "first_name": "Alice",
        "last_name": "Demo",
    },
    {
        "email": "bob@example.com",
        "password": "Password123!",
        "first_name": "Bob",
        "last_name": "Demo",
    },
    {
        "email": "carol@example.com",
        "password": "Password123!",
        "first_name": "Carol",
        "last_name": "Demo",
    },
]


class Command(BaseCommand):
    help = "Creates demo users and sample files for testing."

    def handle(self, *args, **options):

        for data in DEMO_USERS:

            user, created = User.objects.get_or_create(
                username=data["email"],
                defaults={
                    "email": data["email"],
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                },
            )

            if created:
                user.set_password(data["password"])
                user.save()

            filename = "demo_document.txt"

            if not UserFile.objects.filter(
                owner=user,
                original_filename=filename
            ).exists():

                user_file = UserFile.objects.create(
                    owner=user,
                    original_filename=filename,
                )

                user_file.file.save(
                    filename,
                    ContentFile(
                        f"This is a demo file belonging to {data['first_name']}."
                    ),
                    save=True,
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Demo user ready: {data['email']}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo users and files created successfully."
            )
        )