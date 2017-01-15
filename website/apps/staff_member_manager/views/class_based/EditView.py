from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist

from website.apps.staff_member_manager.models import StaffMember
from website.apps.staff_member_manager.utils.create_account_for_staff_member import create_account_for_staff_member
from website.middleware import HttpRedirectException
from website.mixins import LoginRequiredMixin
from website.notification import set_notification, ALERT_DANGER, ALERT_SUCCESS


class EditView(LoginRequiredMixin, TemplateView):
    template_name = "staff_member_manager/edit.html"

    def get(self, request, *args, **kwargs):
        staff_member_id = kwargs["staff_member_id"]

        if staff_member_id == "new":
            return super(EditView, self).get(request, *args, **kwargs)

        try:
            return super(EditView, self).get(request, *args, **kwargs)
        except ObjectDoesNotExist:
            set_notification(request, "staff_member_id of " + staff_member_id + " does not exist.", ALERT_DANGER)

            raise HttpRedirectException(
                reverse("staff_member_manager.browse"),
                "staff_member_id of " + staff_member_id + " does not exist."
            )

    def get_context_data(self, **kwargs):
        context = super(EditView, self).get_context_data(**kwargs)

        staff_member_id = kwargs["staff_member_id"]

        if staff_member_id == "new":
            staff_member = None
        else:
            staff_member = StaffMember.objects.get(id=staff_member_id)

        context["staff_member"] = staff_member

        return context

    @transaction.atomic
    def post(self, request, staff_member_id):
        username = request.POST.get("username", None)
        first_name = request.POST.get("first_name", None)
        last_name = request.POST.get("last_name", None)
        email = request.POST.get("email", None)
        is_active = request.POST.get("is_active", True)
        is_staff = request.POST.get("is_staff", True)
        is_superuser = request.POST.get("is_superuser", True)

        if not username:
            set_notification(request, "Username is required", ALERT_DANGER)

            raise HttpRedirectException(reverse("staff_member_manager.edit", staff_member_id), "Username is required")

        if not email:
            set_notification(request, "Email is required", ALERT_DANGER)

            raise HttpRedirectException(reverse("staff_member_manager.edit", staff_member_id), "Email is required")

        if staff_member_id == "new":
            user = User.objects.create(
                username=username, first_name=first_name, last_name=last_name, email=email, is_active=is_active,
                is_staff=is_staff, is_superuser=is_superuser
            )
            staff_member = StaffMember.objects.create(
                user=user, created_by=request.user.staff_member, updated_by=request.user.staff_member
            )
            staff_member_id = staff_member.id

            set_notification(request, "Created staff member \"" + staff_member.user.username + "\"", ALERT_SUCCESS)

            try:
                create_account_for_staff_member(staff_member)

                set_notification(request, "Created account for \"" + staff_member.user.username + "\"", ALERT_SUCCESS)
            except Exception as error:
                set_notification(
                    request,
                    "Failed to create account for \"" + staff_member.user.username + "\". Error: " + str(error),
                    ALERT_DANGER
                )
        else:
            staff_member = StaffMember.objects.get(id=staff_member_id)
            staff_member.user.username = username
            staff_member.user.first_name = first_name
            staff_member.user.last_name = last_name
            staff_member.user.email = email
            staff_member.user.is_active = is_active
            staff_member.user.is_staff = is_staff
            staff_member.user.is_superuser = is_superuser
            staff_member.user.save()
            staff_member.updated_by = request.user.staff_member
            staff_member.save()

            set_notification(
                request, "Successfully updated staff member \"" + staff_member.user.username + "\"", ALERT_SUCCESS
            )

        return HttpResponseRedirect(
            reverse("staff_member_manager.details", kwargs={"staff_member_id": staff_member_id})
        )
