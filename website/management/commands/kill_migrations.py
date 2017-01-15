import os

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    INIT = "__init__.py"

    class MissingAppModelsDotPathError(Exception):
        pass

    class BadPath(Exception):
        pass

    # def add_arguments(self, parser):
    #     parser.add_argument("app_name", type=str)
    #     parser.add_argument("app_folder", default=None, nargs="?")

    def handle(self, *args, **options):
        if not hasattr(settings, "APP_MODELS_MODULE_PATHS"):
            raise self.MissingAppModelsDotPathError("Settings file is missing APP_MODELS_MODULE_PATHS")

        for app_models_module_path in settings.APP_MODELS_MODULE_PATHS:
            module_path_split = app_models_module_path.split(".")

            if len(module_path_split) < 2:
                raise self.BadPath(
                    "App models module path of \"" + str(app_models_module_path) + "\" is invalid."
                )

            print(module_path_split)

            # Black magic that looks for models in the string and cuts it off and anything after it
            module_path_array = module_path_split[0:module_path_split.index("models")]

            # Get migration_path
            path_list_cuz_python_3_point_4_apparently_sucks_or_something = \
                [settings.BASE_DIR] + module_path_array + ["migrations"]
            migration_path = os.path.join(*path_list_cuz_python_3_point_4_apparently_sucks_or_something)

            # Check if migration_path exists
            if not os.path.exists(migration_path):
                raise self.BadPath("Bad migration path of \"" + migration_path + "\"")

            for the_file in os.listdir(migration_path):
                file_path = os.path.join(migration_path, the_file)

                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as error:
                    print(error)

            # Create init for migrations
            open(os.path.join(migration_path, self.INIT), "w+").close()
