import logging

from django.urls import reverse

from website.apps.account_manager.models import Account
from website.apps.search_filter_sort.views.class_based.BaseBrowseView import BaseBrowseView

logger = logging.getLogger(__name__)


class BrowseView(BaseBrowseView):
    template_name = "account_manager/browse.html"
    model = Account
    filters = []
    sorts = [
        "user__username", "type__name",
    ]
    default_sort_by = ["user__username"]

    def get_context_data(self, **kwargs):
        context = super(BrowseView, self).get_context_data(**kwargs)

        context["object_count"] = self.get_queryset().count()
        context["delete_url"] = reverse("account_manager.delete")

        return context
