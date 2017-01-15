import logging

from django.db import transaction

from website.apps.email_manager.models import EmailBatch, EmailBatchType, EmailBatchStatus, EmailBatchTemplate, \
    EmailInstance, EmailInstanceStatus
from website.apps.email_manager.utils.send_html_email import send_email_batch
from website.global_definitions import EmailBatchTypeNames, EmailBatchStatusNames, EmailBatchTemplateNames, \
    EmailInstanceStatusNames

logger = logging.getLogger(__name__)


@transaction.atomic
def send_email_notification_for_new_staff_member(request, staff_member):
    if staff_member is None:
        raise RuntimeError("staff_member is None")

    if not staff_member.user.email:
        raise RuntimeError("staff_member's email is empty")

    current_staff_member = request.user.staff_member

    email_batch_type = EmailBatchType.objects.get(name=EmailBatchTypeNames.NEW_STAFF_MEMBER_INVITATION)
    email_batch_status = EmailBatchStatus.objects.get(name=EmailBatchStatusNames.PENDING_EMAIL_BATCH_SEND)
    email_batch_template = EmailBatchTemplate.objects.get(name=EmailBatchTemplateNames.NEW_STAFF_MEMBER_INVITATION)

    email_batch = EmailBatch.objects.create(
        type=email_batch_type, status=email_batch_status, template=email_batch_template, created_by=current_staff_member,
        updated_by=current_staff_member
    )

    email_instance_status = EmailInstanceStatus.objects.get(name=EmailInstanceStatusNames.PENDING_EMAIL_INSTANCE_SEND)

    EmailInstance.objects.create(
        batch=email_batch, recipient_email=staff_member.user.email, status=email_instance_status,
        created_by=current_staff_member, updated_by=current_staff_member
    )

    send_email_batch(
        email_batch=email_batch,
        kwargs={"staff_member": staff_member}
    )
