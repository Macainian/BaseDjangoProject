from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.views.generic import TemplateView

from website.apps.email_manager.models import EmailBatchTemplate
from website.middleware import HttpRedirectException
from website.notification import set_notification, ALERT_DANGER


class EmailBatchTemplateEditorView(TemplateView):
    template_name = "email_manager/email_batch_template_edit_and_preview.html"

    def get_context_data(self, **kwargs):
        context = super(EmailBatchTemplateEditorView, self).get_context_data(**kwargs)

        context["email_batch_templates"] = EmailBatchTemplate.objects.filter(is_active=True).order_by("name")
        # context["subjects"] = self.invitation_batch.

        return context

    @transaction.atomic
    def post(self, request, email_batch_template_id):
        # email_batch_template_id = request.POST.get("email_batch_template_id", None)
        #
        # if not email_batch_template_id:
        #     set_notification(request, "email_batch_template_id is required", ALERT_DANGER)
        #
        #     raise HttpRedirectException(
        #         reverse(
        #             "email_manager.email_batch_template_edit_and_preview",
        #             kwargs={"invitation_batch_id": self.invitation_batch.id}
        #         )
        #     )
        #
        # if EmailTemplate.objects.filter(id=email_batch_template_id).exists():
        #     email_batch_template = EmailTemplate.objects.get(id=email_batch_template_id)
        # else:
        #     set_notification(
        #         request, "Email Template with id \"" + self.kwargs["email_batch_template_id"] + "\" does not exist.",
        #         ALERT_DANGER
        #     )
        #
        #     raise HttpRedirectException(
        #         reverse(
        #             "email_manager.email_batch_template_edit_and_preview",
        #             kwargs={"invitation_batch_id": self.invitation_batch.id}
        #         )
        #     )
        #
        # should_assign_email_batch_template = False
        #
        # if self.invitation_batch.email_batch_template:
        #     # If there is already an email template
        #     if self.invitation_batch.email_batch_template.id != email_batch_template_id:
        #         # If the current email template is different from the new one
        #         if self.invitation_batch.status == InvitationBatch.EMAIL_SENT:
        #             # If the invitation batch has already been sent out
        #             set_notification(
        #                 request, "Can't change the email template of an invitation batch that has already been sent out",
        #                 ALERT_DANGER
        #             )
        #
        #             raise HttpRedirectException(
        #                 reverse(
        #                     "email_manager.email_batch_template_edit_and_preview",
        #                     kwargs={"invitation_batch_id": self.invitation_batch.id}
        #                 )
        #             )
        #         else:
        #             # If the invitation batch has never been sent out
        #             should_assign_email_batch_template = True
        # else:
        #     # If there is not already an email template
        #     should_assign_email_batch_template = True
        #
        # if should_assign_email_batch_template:
        #     self.invitation_batch.email_batch_template = email_batch_template
        #     self.invitation_batch.save()

        return HttpResponseRedirect(reverse("email_manager.browse"))
