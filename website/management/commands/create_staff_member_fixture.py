import json
import os
from io import StringIO

from django.core.management.base import BaseCommand
from django.core.management import call_command

from website.settings import BASE_DIR


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("pks", type=str)

    def handle(self, *args, **options):
        pks_option = options["pks"]

        call_command("create_fixture", "auth", "User")
        call_command("create_fixture", "staff_member_manager", "StaffMember")
        call_command("create_fixture", "account_manager", "Account", "apps", pks_option)
