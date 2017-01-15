from django.conf.urls import url

from website.apps.account_manager.views.class_based.BrowseView import BrowseView
from website.apps.account_manager.views.class_based.DeleteView import DeleteView
from website.apps.account_manager.views.class_based.EditView import EditView

urlpatterns = [
    url(r"^browse/$", BrowseView.as_view(), name="account_manager.browse"),
    url(r"^edit/(?P<account_id>.*)/$", EditView.as_view(), name="account_manager.edit"),
    url(r"^delete/$", DeleteView.as_view(), name="account_manager.delete"),

    # url(r"^example_class_view/$", ExampleClassView.as_view(), name="account_manager.example_class_view"),
    # url(r"^example_function_view/$", example_function_view, name="account_manager.example_function_view"),
    # url(r"^example_parameter_passing/(?P<example_var>\w+)/$", example_view, name="account_manager.example_parameter_passing"),
]
