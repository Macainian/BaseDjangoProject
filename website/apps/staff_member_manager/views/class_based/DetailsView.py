from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist

from website.apps.staff_member_manager.models import StaffMember
from website.middleware import HttpRedirectException
from website.mixins import LoginRequiredMixin
from website.notification import set_notification, ALERT_DANGER


class DetailsView(LoginRequiredMixin, TemplateView):
    template_name = "staff_member_manager/details.html"

    def get(self, request, *args, **kwargs):
        staff_member_id = kwargs["staff_member_id"]

        try:
            return super(self.__class__, self).get(request, *args, **kwargs)
        except ObjectDoesNotExist:
            set_notification(
                request, "staff_member_id of " + staff_member_id + " does not exist.", ALERT_DANGER
            )

            raise HttpRedirectException(
                reverse("staff_member_manager.browse"), "staff_member_id of " + staff_member_id + " does not exist."
            )

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)

        staff_member_id = kwargs["staff_member_id"]

        if staff_member_id == "new":
            return HttpResponseRedirect(reverse("staff_member_manager.edit", kwargs={"staff_member_id": staff_member_id}))

        staff_member = StaffMember.objects.get(id=staff_member_id)

        context["staff_member"] = staff_member
        # context["delete_team_member_url"] = reverse("staff_member_manager.delete") + "?id="

        return context
