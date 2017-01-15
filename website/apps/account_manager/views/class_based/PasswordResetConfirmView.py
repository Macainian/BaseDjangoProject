from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from website.apps.account_manager.models import Account
from website.apps.authentication.models import PasswordResetCode
from website.middleware import HttpRedirectException
from website.notification import set_notification, ALERT_DANGER, ALERT_SUCCESS


class PasswordResetConfirmView(TemplateView):
    template_name = "account_manager/password_reset_confirm.html"

    def __init__(self):
        super(PasswordResetConfirmView, self).__init__()

        self.password_reset_code = None
        self.account = None

    def dispatch(self, request, *args, **kwargs):
        uuid = kwargs["uuid"]

        # Check if this code is real
        if PasswordResetCode.objects.filter(id=uuid).exists():
            self.password_reset_code = PasswordResetCode.objects.get(id=uuid)
        else:
            set_notification(request, "Invalid password reset code", ALERT_DANGER)

            raise HttpRedirectException(reverse("login"), "Invalid password reset code")

        # Get the email associated with the EmailInstance associated with this PasswordResetCode
        recipient_email = self.password_reset_code.recipient_email

        # Check if that email address is associated with an Account
        if not Account.objects.filter(user__email=recipient_email).exists():
            set_notification(request, "No account with email of \"" + recipient_email + "\"", ALERT_DANGER)

            raise HttpRedirectException(reverse("login"), "No account with email of \"" + recipient_email + "\"")

        # Set the view's Account to that account so it can be used in the get_context_data() and post()
        self.account = Account.objects.get(user__email=recipient_email)

        return super(PasswordResetConfirmView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PasswordResetConfirmView, self).get_context_data(**kwargs)

        return context

    @transaction.atomic
    def post(self, request, uuid):
        password = request.POST.get("password", None)

        if self.password_reset_code is None:
            raise PermissionDenied

        if self.account is None:
            raise PermissionDenied

        if not password:
            set_notification(request, "Password is required", ALERT_DANGER)

            raise HttpRedirectException(
                reverse("account_manager.password_reset_confirm", kwargs={"uuid": uuid}), "Password is required"
            )

        self.account.user.set_password(password)
        self.account.user.save()

        self.password_reset_code.delete()

        set_notification(request, "Successfully updated account password", ALERT_SUCCESS)

        return HttpResponseRedirect(reverse("login"))
