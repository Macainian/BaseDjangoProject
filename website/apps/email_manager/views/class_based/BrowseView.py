import logging

from django.urls import reverse

from website.apps.email_manager.models import EmailBatch
from website.apps.search_filter_sort.views.class_based.BaseBrowseView import BaseBrowseView

logger = logging.getLogger(__name__)


class BrowseView(BaseBrowseView):
    template_name = "email_manager/browse.html"
    model = EmailBatch
    filters = []
    sorts = ["id", "type__name", "status__name", "template__name", "created_by__username"]
    default_sort_by = ["-id"]

    def get_context_data(self, **kwargs):
        context = super(BrowseView, self).get_context_data(**kwargs)

        context["object_count"] = self.get_queryset().count()
        # context["delete_url"] = reverse("email_manager.delete")

        return context
