from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist

from website.apps.account_manager.models import Account
from website.middleware import HttpRedirectException
from website.mixins import LoginRequiredMixin
from website.notification import set_notification, ALERT_DANGER, ALERT_SUCCESS


class EditView(LoginRequiredMixin, TemplateView):
    template_name = "account_manager/edit.html"

    def get(self, request, *args, **kwargs):
        account_id = kwargs["account_id"]

        if account_id == "new":
            return super(EditView, self).get(request, *args, **kwargs)

        try:
            return super(EditView, self).get(request, *args, **kwargs)
        except ObjectDoesNotExist:
            set_notification(request, "account_id of " + account_id + " does not exist.", ALERT_DANGER)

            raise HttpRedirectException(
                reverse("account_manager.browse"), "account_id of " + account_id + " does not exist."
            )

    def get_context_data(self, **kwargs):
        context = super(EditView, self).get_context_data(**kwargs)

        account_id = kwargs["account_id"]

        if account_id == "new":
            account = None
        else:
            account = Account.objects.get(id=account_id)

        context["account"] = account

        return context

    @transaction.atomic
    def post(self, request, account_id):
        name = request.POST.get("name", None)

        if not name:
            set_notification(request, "Name is required", ALERT_DANGER)

            raise HttpRedirectException(reverse("account_manager.edit", account_id), "Name is required")

        if account_id == "new":
            account = Account.objects.create(name=name)
            account_id = account.id
            set_notification(request, "Created account \"" + account.name + "\"", ALERT_SUCCESS)
        else:
            account = Account.objects.get(id=account_id)
            account.name = name
            account.save()
            set_notification(request, "Successfully updated account", ALERT_SUCCESS)

        return HttpResponseRedirect(reverse("account_manager.edit", kwargs={"account_id": account_id}))
