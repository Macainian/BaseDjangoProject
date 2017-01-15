from django.conf.urls import url

from website.apps.account_manager.views.class_based.BrowseView import BrowseView
from website.apps.account_manager.views.class_based.DeleteView import DeleteView
from website.apps.account_manager.views.class_based.DetailsView import DetailsView
from website.apps.account_manager.views.class_based.EditView import EditView

urlpatterns = [
    url(r"^browse/$", BrowseView.as_view(), name="account_manager.browse"),
    url(r"^edit/(?P<account_id>.*)/$", EditView.as_view(), name="account_manager.edit"),
    url(r"^delete/$", DeleteView.as_view(), name="account_manager.delete"),
    url(r"^details/(?P<account_id>.*)/$", DetailsView.as_view(), name="account_manager.details"),
]
