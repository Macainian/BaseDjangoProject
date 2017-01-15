import fnmatch
import os

from django.core.management.base import BaseCommand
from django.core.management import call_command

from website.settings import BASE_DIR, FIXTURE_LOAD_ORDER


class Command(BaseCommand):
    def handle(self, *args, **options):
        fixture_names = []

        # Get fixture names
        for root, directory_names, file_names in os.walk(BASE_DIR):
            if root.split("\\")[-1] == "fixtures" or root.split("/")[-1] == "fixtures":
                for file_name in fnmatch.filter(file_names, "*.json"):
                    fixture_names.append(file_name)

        # Need to loop in reverse because we will be sorting using insert(0, pop()) which will move that item to the
        # front. If we went in normal order, then StaffMember would be moved to the front first, then the next item
        # would be moved in front of that, thus pushing StaffMember to position 2 and so on as more are added.
        for fixture_name_prefix in reversed(FIXTURE_LOAD_ORDER):
            fixture_name = fixture_name_prefix + ".json"

            if fixture_name in fixture_names:
                fixture_names.insert(0, fixture_names.pop(fixture_names.index(fixture_name)))

        # Load fixtures
        for fixture_name in fixture_names:
            print("\nLoading " + str(fixture_name))
            call_command("loaddata", fixture_name)
