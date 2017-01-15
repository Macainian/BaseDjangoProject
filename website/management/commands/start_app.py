import os

from django.core.management.base import BaseCommand
from django.core.management import call_command
from website.settings import BASE_DIR


class Command(BaseCommand):
    INIT = "__init__.py"
    INSTALLED_APPS_SECTION = "INSTALLED_APPS"
    START_SEARCH_FILTER_SORT_SECTION = "# START SEARCH FILTER SORT MODEL MODULES"
    END_SEARCH_FILTER_SORT_SECTION = "# END SEARCH FILTER SORT MODEL MODULES"
    START_APP_URLS_SECTION = "# START APP URLS"
    END_APP_URLS_SECTION = "# END APP URLS"

    class MissingSettingsFileError(Exception):
        pass

    class BadSettingsFileError(Exception):
        pass

    class MissingUrlsFileError(Exception):
        pass

    class BadUrlsFileError(Exception):
        pass

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str)
        parser.add_argument("app_folder", default=None, nargs="?")

    def handle(self, *args, **options):
        app_name = options["app_name"]
        app_folder_option = options["app_folder"]

# Initial setup
        # If no app_folder_option  was given, default to apps, else use app_folder_option
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

# Create views folder
        # Get views directory
        path_for_views_folder = os.path.join(app_directory, "views")

        # Create views directory
        if not os.path.exists(path_for_views_folder):
            os.makedirs(path_for_views_folder)

        # Create init for views
        open(os.path.join(path_for_views_folder, self.INIT), "w+").close()

# Create class based views
        # Get class_based views directory
        path_for_class_based_folder = os.path.join(path_for_views_folder, "class_based")

        # Create class_based views directory
        if not os.path.exists(path_for_class_based_folder):
            os.makedirs(path_for_class_based_folder)

        # Create init for class_based views
        open(os.path.join(path_for_class_based_folder, self.INIT), "w+").close()

        # Get initial BrowseView.py
        browse_view_file_text = self.get_browse_view_file_text(app_folder, app_name)

        # Create BrowseView.py
        with open(os.path.join(path_for_class_based_folder, "BrowseView.py"), "w+") as browse_view_file:
            browse_view_file.write(browse_view_file_text)

        # Get initial EditView.py
        edit_view_file_text = self.get_edit_view_file_text(app_folder, app_name)

        # Create EditView.py
        with open(os.path.join(path_for_class_based_folder, "EditView.py"), "w+") as edit_view_file:
            edit_view_file.write(edit_view_file_text)

        # Get initial DeleteView.py
        delete_view_file_text = self.get_delete_view_file_text(app_folder, app_name)

        # Create DeleteView.py
        with open(os.path.join(path_for_class_based_folder, "DeleteView.py"), "w+") as delete_view_file:
            delete_view_file.write(delete_view_file_text)

# Create function based views
        # Get function_based views directory
        path_for_function_based_folder = os.path.join(path_for_views_folder, "function_based")

        # Create function_based views directory
        if not os.path.exists(path_for_function_based_folder):
            os.makedirs(path_for_function_based_folder)

        # Create init for function_based views
        open(os.path.join(path_for_function_based_folder, self.INIT), "w+").close()

# Create templates
        # Get templates folder
        path_for_templates_folder = os.path.join(app_directory, "templates", app_name)

        # Create templates directory
        if not os.path.exists(path_for_templates_folder):
            os.makedirs(path_for_templates_folder)

        # Get initial base.html
        templates_base_file_text = self.get_templates_base_file_text(app_name)

        # Create base.html
        with open(os.path.join(path_for_templates_folder, "base.html"), "w+") as base_html_file:
            base_html_file.write(templates_base_file_text)

        # Get initial browse.html
        browse_html_text = self.get_browse_html_text(app_name)

        # Create base.html
        with open(os.path.join(path_for_templates_folder, "browse.html"), "w+") as browse_html_file:
            browse_html_file.write(browse_html_text)

        # Get initial edit.html
        edit_html_text = self.get_edit_html_text(app_name)

        # Create base.html
        with open(os.path.join(path_for_templates_folder, "edit.html"), "w+") as edit_html_file:
            edit_html_file.write(edit_html_text)

# Create static files
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

# Create utils
        # Get utils folder
        path_for_utils_folder = os.path.join(app_directory, "utils")

        # Create utils directory
        if not os.path.exists(path_for_utils_folder):
            os.makedirs(path_for_utils_folder)

        # Create init for utils
        open(os.path.join(path_for_utils_folder, self.INIT), "w+").close()

# Create urls and models
        # Get initial urls.py
        urls_file_text = self.get_urls_file_text(app_folder, app_name)

        # Create urls.py
        with open(os.path.join(app_directory, "urls.py"), "w+") as urls_file:
            urls_file.write(urls_file_text)

        # Get initial models.py
        models_file_text = self.get_models_file_text(app_folder, app_name)

        # Create models.py
        with open(os.path.join(app_directory, "models.py"), "w+") as models_file:
            models_file.write(models_file_text)

# Add stuff to settings and urls
        # Get settings directory
        settings_file_path = os.path.join(BASE_DIR, "website", "settings")

        # Check if the settings file exists
        if not os.path.exists(settings_file_path + ".py"):
            raise self.MissingSettingsFileError(
                "Settings file was not in \"" + settings_file_path + "\" and the app was not registered"
            )

        # Add the app to INSTALLED_APPS
        self.add_app_to_installed_apps(settings_file_path, app_folder, app_name)

        # Add the app to search_filter_sort model modules
        self.add_app_to_search_filter_sort_modules(settings_file_path, app_folder, app_name)

        # Get website urls directory
        website_urls_file_path = os.path.join(BASE_DIR, "website", "urls")

        # Check if the website urls file exists
        if not os.path.exists(website_urls_file_path + ".py"):
            raise self.MissingUrlsFileError(
                "Urls file was not in \"" + website_urls_file_path + "\" and the app was not registered"
            )

        # Add the app to the website url includes
        self.add_app_to_website_url_includes(website_urls_file_path, app_folder, app_name)

    def get_templates_base_file_text(self, app_name):
        # The string below is specifically formatted this way to ensure that it looks correct on the actual file
        # since we are using """
        return \
"""{% extends "base.html" %}

{% block navbar %}
    {% include "navbar.html" with active_nav=""" + '"' + app_name + '" %}' + """
{% endblock %}

{% block extra_css %}
    {% block extra_css_local %}
    {% endblock %}
{% endblock %}

{% block extra_js %}
    {% block extra_js_local %}
    {% endblock %}
{% endblock %}

{% block main_content %}
{% endblock %}"""

    def get_browse_html_text(self, app_name):
        object_name_split = app_name.title().replace("_", " ").replace(" Manager", "")
        object_name_unsplit = app_name.title().replace("_", "").replace("Manager", "")
        object_name_lower_split = app_name.replace("_", " ").replace(" manager", "")
        object_name_lower_unsplit = app_name.replace("_manager", "")
        object_name_lower_dashed = app_name.replace("_", "-").replace("-manager", "")

        # The string below is specifically formatted this way to ensure that it looks correct on the actual file
        # since we are using """
        return \
"""{% extends """ + '"' + app_name + """/base.html" %}

{% load static bootstrap3 query_string notifications tooltip %}

{% block extra_css_local %}
{% endblock %}

{% block extra_js_local %}
    <script>
        var default_pagination = {{ default_pagination }};
        var filter_names = {{ filter_names|safe }};
    </script>

    <script src="{% static 'search_filter_sort/js/search_filter_sort.js' %}" type="text/javascript"></script>
{% endblock %}

{% block main_content %}
    <h2> """ + object_name_split + """s: {{ object_count }} </h2>

    <a class="btn btn-success" href="{% url '""" + app_name + """.edit' """ + object_name_lower_unsplit + """_id='new' %}">
        {% bootstrap_icon "plus" %} Create New """ + object_name_split + """
    </a>

    <button class="btn btn-danger" data-toggle="modal" data-target="#delete-""" + object_name_lower_dashed + """s-modal"
        {% if object_count == 0 %} disabled {% endif %}>
        {% bootstrap_icon "trash" %} Delete """ + object_name_split + """s
    </button>
    <br>
    <br>

    {% include "search_filter_sort/search_filter_sort.html" %}

    <table class="table table-striped">
        <tr>
            {% include "search_filter_sort/checkbox_header.html" %}
            {% include "search_filter_sort/sortable_col.html" with col_title="Example Column" col_type="example_variable_name" is_sortable=True %}
        </tr>

        {% for example_object in object_list %}
            <tr>
                {% include "search_filter_sort/checkbox_row.html" with item_id=example_object.id %}
                <td>{{ example_object.example_variable_name }}</td>
            </tr>
        {% empty %}
        {% endfor %}
    </table>

    {% include "confirmation_modal.html" with name="delete-""" + object_name_lower_dashed + """s" modal_header="Delete """ + object_name_split + """s" modal_body="Are you sure you want to delete these """ + object_name_lower_split + """s?" function='goto_new_url_via_checkboxes("'|add:delete_url|add:'");' confirmation_button_class="btn-danger" confirmation_button_icon="trash" %}
    {% include "search_filter_sort/pagination_page_navigation.html" %}
{% endblock %}"""

    def get_edit_html_text(self, app_name):
        return app_name  # Temp

    def get_urls_file_text(self, app_folder, app_name):
        object_name_lower_unsplit = app_name.replace("_manager", "")

        # The string below is specifically formatted this way to ensure that it looks correct on the actual file
        # since we are using """
        return \
"""from django.conf.urls import url

from website.""" + app_folder + "." + app_name + """.views.class_based.BrowseView import BrowseView
from website.""" + app_folder + "." + app_name + """.views.class_based.DeleteView import DeleteView
from website.""" + app_folder + "." + app_name + """.views.class_based.EditView import EditView

urlpatterns = [
    url(r"^browse/$", BrowseView.as_view(), name=""" + '"' + app_name + """.browse"),
    url(r"^edit/(?P<""" + object_name_lower_unsplit + """_id>.*)/$", EditView.as_view(), name=""" + '"' + app_name + """.edit"),
    url(r"^delete/$", DeleteView.as_view(), name=""" + '"' + app_name + """.delete"),

    # url(r"^example_class_view/$", ExampleClassView.as_view(), name=""" + '"' + app_name + """.example_class_view"),
    # url(r"^example_function_view/$", example_function_view, name=""" + '"' + app_name + """.example_function_view"),
    # url(r"^example_parameter_passing/(?P<example_var>\w+)/$", example_view, name=""" + '"' + app_name + """.example_parameter_passing"),
]
"""

    def get_models_file_text(self, app_folder, app_name):
        # The string below is specifically formatted this way to ensure that it looks correct on the actual file
        # since we are using """
        return \
"""from django.db import models
from django.conf import settings

MODELS_MODULE_PATH = settings.""" + app_folder.upper() + "_" + app_name.upper() + """_MODELS_MODULE_PATH

# Anywhere you see default=None, this is being used to force integrity error if this is not supplied on creation


"""

    def get_browse_view_file_text(self, app_folder, app_name):
        object_name_unsplit = app_name.title().replace("_", "").replace("Manager", "")

        # The string below is specifically formatted this way to ensure that it looks correct on the actual file
        # since we are using """
        return \
"""import logging

from django.urls import reverse

from website.""" + app_folder + "." + app_name + """.models import """ + object_name_unsplit + """
from website.apps.search_filter_sort.views.class_based.BaseBrowseView import BaseBrowseView

logger = logging.getLogger(__name__)


class BrowseView(BaseBrowseView):
    template_name = """ + '"' + app_name + """/browse.html"
    model = """ + object_name_unsplit + """
    filters = []
    sorts = ["id"]
    default_sort_by = ["-id"]

    def get_context_data(self, **kwargs):
        context = super(BrowseView, self).get_context_data(**kwargs)

        context["object_count"] = self.get_queryset().count()
        context["delete_url"] = reverse(""" + '"' + app_name + """.delete")

        return context
"""

    def get_edit_view_file_text(self, app_folder, app_name):
        object_name_unsplit = app_name.title().replace("_", "").replace("Manager", "")
        object_name_lower_split = app_name.replace("_", " ").replace(" manager", "")
        object_name_lower_unsplit = app_name.replace("_manager", "")

        # The string below is specifically formatted this way to ensure that it looks correct on the actual file
        # since we are using """
        return \
"""from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist

from website.""" + app_folder + "." + app_name + ".models import " + object_name_unsplit + """
from website.middleware import HttpRedirectException
from website.mixins import LoginRequiredMixin
from website.notification import set_notification, ALERT_DANGER, ALERT_SUCCESS


class EditView(LoginRequiredMixin, TemplateView):
    template_name = """ + '"' + app_name + """/edit.html"

    def get(self, request, *args, **kwargs):
        """ + object_name_lower_unsplit + """_id = kwargs[""" + '"' + object_name_lower_unsplit + """_id"]

        if """ + object_name_lower_unsplit + """_id == "new":
            return super(EditView, self).get(request, *args, **kwargs)

        try:
            return super(EditView, self).get(request, *args, **kwargs)
        except ObjectDoesNotExist:
            set_notification(request, """ + '"' + object_name_lower_unsplit + """_id of " + """ + object_name_lower_unsplit + """_id + " does not exist.", ALERT_DANGER)

            raise HttpRedirectException(
                reverse(""" + '"' + object_name_lower_unsplit + """_manager.browse"),
                """ + '"' + object_name_lower_unsplit + """_id of " + """ + object_name_lower_unsplit + """_id + " does not exist."
            )

    def get_context_data(self, **kwargs):
        context = super(EditView, self).get_context_data(**kwargs)

        """ + object_name_lower_unsplit + """_id = kwargs[""" + '"' + object_name_lower_unsplit + """_id"]

        if """ + object_name_lower_unsplit + """_id == "new":
            """ + object_name_lower_unsplit + """ = None
        else:
            """ + object_name_lower_unsplit + " = " + object_name_unsplit + """.objects.get(id=""" + object_name_lower_unsplit + """_id)

        context[""" + '"' + object_name_lower_unsplit + """"] = """ + object_name_lower_unsplit + """

        return context

    @transaction.atomic
    def post(self, request, """ + object_name_lower_unsplit + """_id):
        name = request.POST.get("name", None)

        if not name:
            set_notification(request, "Name is required", ALERT_DANGER)

            raise HttpRedirectException(reverse(""" + '"' + object_name_lower_unsplit + """_manager.edit", """ + object_name_lower_unsplit + """_id), "Name is required")

        if """ + object_name_lower_unsplit + """_id == "new":
            """ + object_name_lower_unsplit + """ = """ + object_name_unsplit + """.objects.create(name=name, created_by_id=request.user.REPLACE_THIS)
            """ + object_name_lower_unsplit + """_id = """ + object_name_lower_unsplit + """.id
            set_notification(request, "Created """ + object_name_unsplit + """ \\"" + """ + object_name_lower_unsplit + """.name + "\\"", ALERT_SUCCESS)
        else:
            """ + object_name_lower_unsplit + """ = """ + object_name_unsplit + """.objects.get(id=""" + object_name_lower_unsplit + """_id)
            """ + object_name_lower_unsplit + """.name = name
            """ + object_name_lower_unsplit + """.save()
            set_notification(
                request, "Successfully updated """ + object_name_unsplit + """ \\"" + """ + object_name_lower_unsplit + """.name + "\\"", ALERT_SUCCESS
            )

        return HttpResponseRedirect(
            reverse(""" + '"' + object_name_lower_unsplit + """_manager.edit", kwargs={""" + '"' + object_name_lower_unsplit + """_id": """ + object_name_lower_unsplit + """_id})
        )
"""

    def get_delete_view_file_text(self, app_folder, app_name):
        object_name_lower_split = app_name.replace("_", " ").replace(" manager", "")

        # The string below is specifically formatted this way to ensure that it looks correct on the actual file
        # since we are using """
        return \
"""import logging

from django.core.urlresolvers import reverse
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseRedirect

from website.""" + app_folder + "." + app_name + """.views.class_based.BrowseView import BrowseView
from website.middleware import HttpRedirectException
from website.notification import set_notification, ERROR_LOG, create_notification_log, SUCCESS_LOG, ALERT_DANGER, """ + "\\" + """
    ALERT_SUCCESS

logger = logging.getLogger(__name__)


class DeleteView(BrowseView):
    def get(self, *args, **kwargs):
        items = self.get_queryset()
        error_log = []
        success_log = []

        if items.count() == 0:
            set_notification(self.request, "There were no """ + object_name_lower_split + "s" + """ selected to delete", ALERT_DANGER)

            raise HttpRedirectException(reverse(""" + '"' + app_name + """.browse"))

        items_deleted_count = 0
        items_protected_count = 0

        for item in items:
            try:
                temp_id = item.id
                item.delete()
                items_deleted_count += 1
                success_log.append("ID " + str(temp_id) + ": Deleted successfully")
            except ProtectedError as error:
                logger.info(str(error))
                error_log.append("ID " + str(item.id) + ": " + (error[0]))
                items_protected_count += 1

        if items_deleted_count == 0:
            set_notification(
                self.request,
                "Failed to delete " + str(items_protected_count) + " """ + object_name_lower_split + "s" + """ due to protection <br>" +
                    create_notification_log(error_log, 1, ERROR_LOG),
                ALERT_DANGER
            )
        else:
            set_notification(
                self.request,
                "Successfully deleted " + str(items_deleted_count) + " """ + object_name_lower_split + "s" + """ <br>" +
                    create_notification_log(success_log, 1, SUCCESS_LOG),
                ALERT_SUCCESS
            )

            if len(error_log) > 0:
                set_notification(
                    self.request,
                    "Failed to delete " + str(items_protected_count) + " """ + object_name_lower_split + "s" + """ due to protection<br>" +
                        create_notification_log(error_log, 2, ERROR_LOG),
                    ALERT_DANGER
                )

        return HttpResponseRedirect(reverse(""" + '"' + app_name + """.browse"))
"""

    def add_app_to_installed_apps(self, settings_file_path, app_folder, app_name):
        have_found_installed_apps_section = False

        # Build up a new settings file into an array
        with open(settings_file_path + ".py", "r") as settings_file:
            app_has_been_added = False
            new_lines = []
            last_non_comment_line = ""
            last_non_comment_line_index = -1

            for line in settings_file:
                if not app_has_been_added:
                    stripped_line = line.strip()

                    if self.INSTALLED_APPS_SECTION in line:
                        have_found_installed_apps_section = True

                    if have_found_installed_apps_section:
                        if stripped_line != ")":
                            # ^If this is not the end of the installed apps section
                            if not stripped_line.startswith("#"):
                                # ^If this line is not commented out
                                last_non_comment_line = line
                                last_non_comment_line_index = len(new_lines)

                                if not stripped_line.endswith(","):
                                    # ^If this line does not end with a comma (thus is not ready to accept more apps
                                    # into the list)
                                    last_non_comment_line += ","
                        else:
                            # ^If this is the end of the installed apps section
                            new_lines[last_non_comment_line_index] = last_non_comment_line
                            new_lines.append("    \"website." + app_folder + "." + app_name + "\",\n")
                            app_has_been_added = True

                new_lines.append(line)

        if not have_found_installed_apps_section:
            raise self.BadSettingsFileError("Bad Settings File: Missing \"" + self.INSTALLED_APPS_SECTION + "\"")

        if not app_has_been_added:
            raise self.BadSettingsFileError(
                "Bad Settings File: Missing \")\" for \"" + self.INSTALLED_APPS_SECTION + "\" section"
            )

        # Overwrite settings file to add the new app using the array of new_lines
        with open(settings_file_path + ".py", "w") as settings_file:
            settings_file.writelines(new_lines)

    def add_app_to_search_filter_sort_modules(self, settings_file_path, app_folder, app_name):
        have_found_search_filter_sort_modules_section = False

        # Build up a new settings file into an array
        with open(settings_file_path + ".py", "r") as settings_file:
            app_has_been_added = False
            new_lines = []
            last_non_comment_line = ""
            last_non_comment_line_index = -1

            for line in settings_file:
                if not app_has_been_added:
                    stripped_line = line.strip()

                    if stripped_line == self.START_SEARCH_FILTER_SORT_SECTION:
                        have_found_search_filter_sort_modules_section = True

                    if have_found_search_filter_sort_modules_section:
                        if stripped_line != self.END_SEARCH_FILTER_SORT_SECTION:
                            # ^If this is not the end of the search filter sort section
                            if not stripped_line.startswith("#"):
                                # ^If this line is not commented out
                                last_non_comment_line = line
                                last_non_comment_line_index = len(new_lines)
                        else:
                            # ^If this is the end of the search filter sort section
                            new_lines[last_non_comment_line_index] = last_non_comment_line
                            new_lines.append(
                                app_folder.upper() + "_" + app_name.upper() + "_MODELS_MODULE_PATH = \"website." +
                                app_folder + "." + app_name + ".models\"\n"
                            )
                            app_has_been_added = True

                new_lines.append(line)

            if not have_found_search_filter_sort_modules_section:
                raise self.BadSettingsFileError(
                    "Bad Settings File: Missing \"" + self.START_SEARCH_FILTER_SORT_SECTION + "\""
                )

            if not app_has_been_added:
                raise self.BadSettingsFileError(
                    "Bad Settings File: Missing \"" + self.END_SEARCH_FILTER_SORT_SECTION + "\""
                )

        # Overwrite settings file to add the new app using the array of new_lines
        with open(settings_file_path + ".py", "w") as settings_file:
            settings_file.writelines(new_lines)

    def add_app_to_website_url_includes(self, urls_file_path, app_folder, app_name):
        have_found_app_urls_section = False

        # Build up a new urls file into an array
        with open(urls_file_path + ".py", "r") as urls_file:
            app_has_been_added = False
            new_lines = []
            last_non_comment_line = ""
            last_non_comment_line_index = -1

            for line in urls_file:
                if not app_has_been_added:
                    stripped_line = line.strip()

                    if stripped_line == self.START_APP_URLS_SECTION:
                        have_found_app_urls_section = True

                    if have_found_app_urls_section:
                        if stripped_line != self.END_APP_URLS_SECTION:
                            # ^If this is not the end of the app urls section
                            if not stripped_line.startswith("#"):
                                # ^If this line is not commented out
                                last_non_comment_line = line
                                last_non_comment_line_index = len(new_lines)
                        else:
                            # ^If this is the end of the app urls section
                            new_lines[last_non_comment_line_index] = last_non_comment_line
                            new_lines.append(
                                "    url(r\"^" + app_name + "/\", include(\"website." + app_folder + "." + app_name +
                                ".urls\")),\n"
                            )
                            app_has_been_added = True

                new_lines.append(line)

            if not have_found_app_urls_section:
                raise self.BadUrlsFileError(
                    "Bad Urls File: Missing \"" + self.START_APP_URLS_SECTION + "\""
                )

            if not app_has_been_added:
                raise self.BadSettingsFileError(
                    "Bad Urls File: Missing \"" + self.END_APP_URLS_SECTION + "\""
                )

        # Overwrite urls file to add the new app using the array of new_lines
        with open(urls_file_path + ".py", "w") as urls_file:
            urls_file.writelines(new_lines)
