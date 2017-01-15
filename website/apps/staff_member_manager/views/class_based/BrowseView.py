import logging

from django.urls import reverse

from website.apps.staff_member_manager.models import StaffMember
from website.apps.search_filter_sort.views.class_based.BaseBrowseView import BaseBrowseView

logger = logging.getLogger(__name__)


class BrowseView(BaseBrowseView):
    template_name = "staff_member_manager/browse.html"
    model = StaffMember
    filters = []
    sorts = [
        "id", "user__username", "user__last_name", "user__email", "user__date_joined", "created_by__user__username"
    ]
    default_sort_by = ["-id"]

    def get_context_data(self, **kwargs):
        context = super(BrowseView, self).get_context_data(**kwargs)

        create_staff_member_fixture_command = "create_staff_member_fixture "

        for staff_member in StaffMember.objects.all():
            if hasattr(staff_member.user, "account"):
                create_staff_member_fixture_command += str(staff_member.user.account.id) + ","

        create_staff_member_fixture_command = create_staff_member_fixture_command[:-1]

        context["object_count"] = self.get_queryset().count()
        context["delete_url"] = reverse("staff_member_manager.delete")
        context["create_staff_member_fixture_command"] = create_staff_member_fixture_command

        return context
