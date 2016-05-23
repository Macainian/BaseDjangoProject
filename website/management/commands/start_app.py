import os

from django.core.management.base import BaseCommand
from django.core.management import call_command
from website.settings import BASE_DIR


class Command(BaseCommand):
    INIT = "__init__.py"

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str)
        parser.add_argument("app_folder", default=None, nargs="?")

    def handle(self, *args, **options):
        app_name = options["app_name"]
        app_folder_option = options["app_folder"]

        if app_folder_option is None:
            app_folder = "apps"
        else:
            app_folder = app_folder_option

        # Get app directory
        app_directory = os.path.join(BASE_DIR, "website", app_folder, app_name)

        # Create app directory
        if not os.path.exists(app_directory):
            os.makedirs(app_directory)

        # Create initial app
        call_command("startapp", app_name, app_directory)

        # Delete views file
        os.remove(os.path.join(app_directory, "views.py"))

        # Get views directory
        path_for_views_folder = os.path.join(app_directory, "views")

        # Create views directory
        if not os.path.exists(path_for_views_folder):
            os.makedirs(path_for_views_folder)

        # Create init for views
        open(os.path.join(path_for_views_folder, self.INIT), "w+").close()

        # Get class_based views directory
        path_for_class_based_folder = os.path.join(path_for_views_folder, "class_based")

        # Create class_based views directory
        if not os.path.exists(path_for_class_based_folder):
            os.makedirs(path_for_class_based_folder)

        # Create init for class_based views
        open(os.path.join(path_for_class_based_folder, self.INIT), "w+").close()

        # Get function_based views directory
        path_for_function_based_folder = os.path.join(path_for_views_folder, "function_based")

        # Create function_based views directory
        if not os.path.exists(path_for_function_based_folder):
            os.makedirs(path_for_function_based_folder)

        # Create init for function_based views
        open(os.path.join(path_for_function_based_folder, self.INIT), "w+").close()

        # Get templates folder
        path_for_templates_folder = os.path.join(app_directory, "templates", app_name)

        # Create templates directory
        if not os.path.exists(path_for_templates_folder):
            os.makedirs(path_for_templates_folder)

        # Get initial base.html. The string below is specifically formatted this way to ensure that it looks correct on the actual file since we are using """
        templates_base_file_text = \
"""{% extends "base.html" %}

{% block navbar %}
    {% include "navbar.html" with active_nav=""" + '"' + app_name + '" %}' + """
{% endblock %}

{% block extra_css %}
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">

    {% block extra_css_local %}
    {% endblock %}
{% endblock %}

{% block extra_js %}
    {% block extra_js_local %}
    {% endblock %}
{% endblock %}

{% block main_content %}
{% endblock %}"""

        # Create base.html
        base_html_file = open(os.path.join(path_for_templates_folder, "base.html"), "w+")
        base_html_file.write(templates_base_file_text)
        base_html_file.close()

        # Get static folder
        path_for_static_folder = os.path.join(app_directory, "static", app_name)

        # Create static directory
        if not os.path.exists(path_for_static_folder):
            os.makedirs(path_for_static_folder)

        # Get css folder
        path_for_css_folder = os.path.join(path_for_static_folder, "css")

        # Create css directory
        if not os.path.exists(path_for_css_folder):
            os.makedirs(path_for_css_folder)

        # Create temp.css
        open(os.path.join(path_for_css_folder, "temp.css"), "w+").close()

        # Get js folder
        path_for_js_folder = os.path.join(path_for_static_folder, "js")

        # Create js directory
        if not os.path.exists(path_for_js_folder):
            os.makedirs(path_for_js_folder)

        # Create temp.js
        open(os.path.join(path_for_js_folder, "temp.js"), "w+").close()

        # Get utils folder
        path_for_utils_folder = os.path.join(app_directory, "utils")

        # Create utils directory
        if not os.path.exists(path_for_utils_folder):
            os.makedirs(path_for_utils_folder)

        # Create init for utils
        open(os.path.join(path_for_utils_folder, self.INIT), "w+").close()

        # Get initial urls.py. The string
        urls_file_text = \
"""from django.conf.urls import url

urlpatterns = [
    # url(r"^example_class_view/$", ExampleClassView.as_view(), name=""" + '"' + app_name + """.example_class_view"),
    # url(r"^example_function_view/$", example_function_view, name=""" + '"' + app_name + """.example_function_view"),
    # url(r"^example_parameter_passing/(?P<example_var>\w+)/$", example_view, name=""" + '"' + app_name + """.example_parameter_passing"),
]"""

        # Create urls.py
        urls_file = open(os.path.join(app_directory, "urls.py"), "w+")
        urls_file.write(urls_file_text)
        urls_file.close()

        # Get app directory
        settings_file_path = os.path.join(BASE_DIR, "website", "settings")

        if not os.path.exists(settings_file_path + ".py"):
            print("Settings file was not in \"" + settings_file_path + "\" and the app was not registered")

        # Build up a new settings file into an array
        with open(settings_file_path + ".py", "r") as settings_file:
            have_found_installed_apps_section = False
            app_has_been_added = False
            new_lines = []
            last_non_comment_line = ""
            last_non_comment_line_index = -1

            for line in settings_file:
                if not app_has_been_added:
                    stripped_line = line.strip()

                    if "INSTALLED_APPS" in line:
                        have_found_installed_apps_section = True

                    if have_found_installed_apps_section:
                        # If this is not the end of the installed apps section
                        if stripped_line != ")":
                            # If this line is not commented out
                            if not stripped_line.startswith("#"):
                                last_non_comment_line = line
                                last_non_comment_line_index = len(new_lines)

                                # If this line does not end with a comma (thus is not ready to accept more apps into the list)
                                if not stripped_line.endswith(","):
                                    last_non_comment_line += ","
                        else:  # If this is the end of the installed apps section
                            new_lines[last_non_comment_line_index] = last_non_comment_line
                            new_lines.append("    \"website." + app_folder + "." + app_name + "\",\n")
                            app_has_been_added = True

                new_lines.append(line)

        # Overwrite settings file to add the new app using the array of new_lines
        with open(settings_file_path + ".py", "w") as settings_file:
            settings_file.writelines(new_lines)
