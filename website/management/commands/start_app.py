import os

from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    INIT = "__init__.py"

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str)

    def handle(self, *args, **options):
        app_name = options["app_name"]

        # Get app directory
        base_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        app_directory = os.path.join(base_directory, "website", "apps", app_name)

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