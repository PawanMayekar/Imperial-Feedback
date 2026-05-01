"""
Create or update a UserMaster account for the /admin reviewer console.

Usage:
    python manage.py create_admin
    python manage.py create_admin --username alex --password "..." --full-name "Alex"
    python manage.py create_admin --username alex --reset-password
"""

from getpass import getpass

from django.core.management.base import BaseCommand, CommandError

from feedback.models import UserMaster


class Command(BaseCommand):
    help = "Create or update a UserMaster account used for the /admin reviewer panel."

    def add_arguments(self, parser):
        parser.add_argument("--username", help="Username (will prompt if omitted)")
        parser.add_argument("--password", help="Password (will prompt securely if omitted)")
        parser.add_argument("--email", default="", help="Email address (optional)")
        parser.add_argument("--full-name", dest="full_name", default="", help="Display name (optional)")
        parser.add_argument(
            "--reset-password",
            action="store_true",
            help="If the username already exists, update the password instead of failing.",
        )

    def handle(self, *args, **options):
        username = options.get("username") or input("Username: ").strip()
        if not username:
            raise CommandError("Username is required.")

        existing = UserMaster.objects.filter(username=username).first()
        if existing and not options["reset_password"]:
            raise CommandError(
                f'User "{username}" already exists. '
                f"Use --reset-password to update their password."
            )

        password = options.get("password")
        if not password:
            password = getpass("Password: ")
            confirm = getpass("Confirm password: ")
            if password != confirm:
                raise CommandError("Passwords do not match.")
        if len(password) < 6:
            raise CommandError("Password must be at least 6 characters.")

        user = existing or UserMaster(username=username)
        if not existing:
            user.email = options["email"]
            user.full_name = options["full_name"]
        else:
            if options["email"]:
                user.email = options["email"]
            if options["full_name"]:
                user.full_name = options["full_name"]

        user.set_password(password)
        user.is_active = True
        user.save()

        action = "updated" if existing else "created"
        self.stdout.write(self.style.SUCCESS(f'User "{username}" {action} successfully.'))
