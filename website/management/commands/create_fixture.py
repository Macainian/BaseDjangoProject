import json
import os
from io import StringIO

from django.core.management.base import BaseCommand
from django.core.management import call_command

from website.settings import BASE_DIR


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str)
        parser.add_argument("model_name", type=str)
        parser.add_argument("app_folder", default=None, nargs="?")
        parser.add_argument("pks", default=None, nargs="?")

    def handle(self, *args, **options):
        app_name = options["app_name"]
        model_name = options["model_name"]
        app_folder_option = options["app_folder"]
        pks_option = options["pks"]
        extension = ".json"

        # If no app_folder_option  was given, default to apps, else use app_folder_option
        if app_folder_option is None:
            app_folder = "apps"
        else:
            if app_folder_option.startswith(("1", "2", "3", "4", "5", "6", "7", "8", "9")):
                raise RuntimeError("Bad app_folder. Were you trying to use pks? If so, use app_folder as well.")

            app_folder = app_folder_option

        # Create fixture in text file-like form
        fixture_text = StringIO()

        if pks_option is None:
            call_command(
                "dumpdata", app_name + "." + model_name, stdout=fixture_text
            )
        else:
            call_command(
                "dumpdata", app_name + "." + model_name, "--pks", pks_option, stdout=fixture_text
            )

        fixture_text.seek(0)

        if app_name == "auth":
            app_name = "website"

        # Get fixtures folder
        if app_name == "website":
            fixtures_folder = os.path.join(BASE_DIR, app_name, "fixtures")
        else:
            fixtures_folder = os.path.join(BASE_DIR, "website", app_folder, app_name, "fixtures")

        # Create fixtures folder if it doesn't exist
        if not os.path.exists(fixtures_folder):
            os.makedirs(fixtures_folder)

        with open(os.path.join(fixtures_folder, model_name + extension), "w+") as fixture_file:
            fixture = json.load(fixture_text)
            json.dump(fixture, fixture_file, sort_keys=True, indent=4)
