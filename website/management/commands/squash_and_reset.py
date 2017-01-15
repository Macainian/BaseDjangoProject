from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command("kill_migrations")
        call_command("makemigrations")
        call_command("reset_db", "--nodata", "--nobackup")
        # call_command("create_admin_account_migration")
        call_command("migrate")
        call_command("load_fixtures")
