from __future__ import unicode_literals

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
