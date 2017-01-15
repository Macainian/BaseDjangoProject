from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist

from website.apps.email_manager.models import Email
from website.middleware import HttpRedirectException
from website.mixins import LoginRequiredMixin
from website.notification import set_notification, ALERT_DANGER, ALERT_SUCCESS


class EditView(LoginRequiredMixin, TemplateView):
    template_name = "email_manager/edit.html"

    def get(self, request, *args, **kwargs):
        email_id = kwargs["email_id"]

        if email_id == "new":
            return super(EditView, self).get(request, *args, **kwargs)

        try:
            return super(EditView, self).get(request, *args, **kwargs)
        except ObjectDoesNotExist:
            set_notification(request, "email_id of " + email_id + " does not exist.", ALERT_DANGER)

            raise HttpRedirectException(
                reverse("email_manager.browse"),
                "email_id of " + email_id + " does not exist."
            )

    def get_context_data(self, **kwargs):
        context = super(EditView, self).get_context_data(**kwargs)

        email_id = kwargs["email_id"]

        if email_id == "new":
            email = None
        else:
            email = Email.objects.get(id=email_id)

        context["email"] = email

        return context

    @transaction.atomic
    def post(self, request, email_id):
        name = request.POST.get("name", None)

        if not name:
            set_notification(request, "Name is required", ALERT_DANGER)

            raise HttpRedirectException(reverse("email_manager.edit", email_id), "Name is required")

        if email_id == "new":
            email = Email.objects.create(name=name, created_by_id=1)
            email_id = email.id
            set_notification(request, "Created email \"" + email.name + "\"", ALERT_SUCCESS)
        else:
            email = Email.objects.get(id=email_id)
            email.name = name
            email.save()
            set_notification(request, "Successfully updated email", ALERT_SUCCESS)

        return HttpResponseRedirect(
            reverse("email_manager.edit", kwargs={"email_id": email_id})
        )
