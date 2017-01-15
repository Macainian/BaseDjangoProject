import os

from django.core.management.base import BaseCommand
from website.settings import BASE_DIR


class Command(BaseCommand):
    def handle(self, *args, **options):
        migrations_folder = os.path.join(BASE_DIR, "website", "migrations")

        admin_account_migration_text = self.get_admin_account_migration_text()

        # Create BrowseView.py
        with open(os.path.join(migrations_folder, "0001_initial.py"), "w+") as admin_account_migration_file:
            admin_account_migration_file.write(admin_account_migration_text)

    def get_admin_account_migration_text(self):
        # The string below is specifically formatted this way to ensure that it looks correct on the actual file
        # since we are using """
        return \
"""from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import migrations

from website.apps.staff_member_manager.models import StaffMember


def add_staff_members(apps, schema_editor):
    if not StaffMember.objects.filter(user__username="admin").exists():
        user = User.objects.create(username="admin")
        staff_member = StaffMember.objects.create(user=user)
        staff_member.user.is_staff = True
        staff_member.user.is_active = True
        staff_member.user.is_superuser = True
        staff_member.user.set_password("1")
        staff_member.generated_password = ""
        staff_member.user.first_name = "System"
        staff_member.user.last_name = "Superuser"
        staff_member.user.save()
        staff_member.save()


class Migration(migrations.Migration):
    dependencies = [
        ("staff_member_manager", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_staff_members),
    ]
"""