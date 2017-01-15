import socket
import logging

from django.core.mail import mail_managers, send_mail
from django.conf import settings

from website.apps.email_manager.models import DoNotSendEmailList, EmailBatchType, EmailBatchStatus, EmailInstanceStatus
from website.apps.email_manager.utils.errors import EmailsAreDisabledError, NoRecipientsError, TooManyRecipientsError, \
    FailedToSendEmailError, MailServerIsDownError
from website.apps.email_manager.utils.get_clean_ckeditor_html_code import get_clean_ckeditor_html_code
from website.global_definitions import EmailBatchTypeNames, EmailBatchStatusNames, EmailInstanceStatusNames

logger = logging.getLogger(__name__)


def send_email_batch(email_batch, **kwargs):
    for email_instance in email_batch.email_instances.all():
        if not email_instance.sent_datetime:
            try:
                send_html_email(email_batch=email_batch, email_instance=email_instance, **kwargs)
            except EmailsAreDisabledError as error:
                raise error
            except NoRecipientsError as error:
                raise error
            except TooManyRecipientsError as error:
                raise error
            except FailedToSendEmailError as error:
                raise error

    email_batch.status = EmailBatchStatus.objects.get(name=EmailBatchStatusNames.EMAIL_BATCH_SENT_COMPLETELY)
    email_batch.save()


# todo: Fix this so it can do more than one recipient. Originally this was supposed to handle all kinds of emails, but
# todo: as a shortcut, it was hacked to not allow more than 1 recipient. This should be fixed later to allow more than
# todo: 1 recipient.
def send_html_email(email_batch, email_instance, should_send_to_managers=False, subject_code=None,
                    from_code=None, basic_message=None, **kwargs):
    if settings.DISABLE_SEND_HTML_EMAIL:
        error_message = "Email delivery is disabled, DISABLE_SEND_HTML_EMAIL=True"
        logger.error(error_message)

        raise EmailsAreDisabledError(error_message)

    # todo: Fix this shit so that it can actually use more than one email.
    recipient_emails = email_instance.recipient_email

    if not isinstance(recipient_emails, list):
        if recipient_emails is not None:
            recipient_emails = [recipient_emails]

    if not recipient_emails:
        error_message = "Recipient list was empty"
        logger.error(error_message)

        raise NoRecipientsError(error_message)

    forgot_password_email_batch_type = EmailBatchType.objects.get(name=EmailBatchTypeNames.FORGOT_PASSWORD)
    forgot_username_email_batch_type = EmailBatchType.objects.get(name=EmailBatchTypeNames.FORGOT_USERNAME)
    new_staff_member_invitation_email_batch_type = EmailBatchType.objects.get(name=EmailBatchTypeNames.NEW_STAFF_MEMBER_INVITATION)
    new_user_registration_email_batch_type = EmailBatchType.objects.get(name=EmailBatchTypeNames.NEW_USER_REGISTRATION)
    non_filterable_email_batch_types = [
        forgot_password_email_batch_type, forgot_username_email_batch_type, new_staff_member_invitation_email_batch_type,
        new_user_registration_email_batch_type
    ]

    # Filter people who are on a Do Not Send Email list unless this is a special type of email like Forgot Password.
    if email_batch.type not in non_filterable_email_batch_types:
        non_filtered_recipient_emails = []

        for recipient_email in recipient_emails:
            if DoNotSendEmailList.objects.filter(email__iexact=recipient_email).exists():
                logger.info("%s is on Do Not Send Email list, skipping" % recipient_email)
            else:
                non_filtered_recipient_emails.append(recipient_email)

        recipient_emails = non_filtered_recipient_emails

    if not recipient_emails:
        error_message = "All recipient_emails were on the Do Not Send Email list"
        logger.error(error_message)

        raise NoRecipientsError(error_message)

    # todo: Fix this shit so it can send to more than 1 recipient
    if len(recipient_emails) > 1:
        error_message = "Can't send to more than 1 recipient"
        logger.error(error_message)

        raise TooManyRecipientsError(error_message)

    final_html_code = get_clean_ckeditor_html_code(
        unparsed_injected_html_code=email_batch.template.html_code, context=kwargs["kwargs"]  # I don't get it either :D
    )

    if subject_code is None:
        subject_code = email_batch.template.subject_code

    if from_code is None:
        if email_batch.template.from_code:
            from_code = email_batch.template.from_code
        else:
            from_code = settings.DEFAULT_FROM_EMAIL

    if basic_message is None:
        basic_message = email_batch.template.basic_message

    try:
        if should_send_to_managers:
            mail_managers(subject_code, message=basic_message, html_message=final_html_code, fail_silently=False)

        did_succeed = send_mail(
            subject_code, basic_message, from_code, recipient_emails, html_message=final_html_code, fail_silently=False
        )

        if not did_succeed:
            error_message = "Can't send email to %s" % recipient_emails
            logger.error(error_message)

            raise FailedToSendEmailError(error_message)
    except socket.error as error:
        error_message = "Mail server may be down. Socket error: %s" % error
        logger.error(error_message)

        raise MailServerIsDownError(error_message)
    except Exception as error:
        error_message = "Failed to send an email to %s" % recipient_emails
        logger.critical("Exception in send_html_email. Stacktrace is below for your convenience")
        logger.exception(error)

        raise FailedToSendEmailError(error_message)

    email_instance.status = EmailInstanceStatus.objects.get(name=EmailInstanceStatusNames.EMAIL_INSTANCE_SENT)
    email_instance.save()

    logger.info("Successfully sent email to %s" % recipient_emails)
