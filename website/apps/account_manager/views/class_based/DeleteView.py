import logging

from django.core.urlresolvers import reverse
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseRedirect

from website.apps.account_manager.views.class_based.BrowseView import BrowseView
from website.middleware import HttpRedirectException
from website.notification import set_notification, ERROR_LOG, create_notification_log, SUCCESS_LOG, ALERT_DANGER, \
    ALERT_SUCCESS

logger = logging.getLogger(__name__)


class DeleteView(BrowseView):
    def get(self, *args, **kwargs):
        items = self.get_queryset()
        error_log = []
        success_log = []

        if items.count() == 0:
            set_notification(self.request, "There were no accounts selected to delete", ALERT_DANGER)

            raise HttpRedirectException(reverse("account_manager.browse"))

        items_deleted_count = 0
        items_protected_count = 0

        for item in items:
            try:
                temp_id = item.id
                item.delete()
                items_deleted_count += 1
                success_log.append("ID " + temp_id + ": Deleted successfully")
            except ProtectedError as error:
                logger.info(str(error))
                error_log.append("ID " + item.id + ": " + (error[0]))
                items_protected_count += 1

        if items_deleted_count == 0:
            set_notification(
                self.request,
                "Failed to delete " + str(items_protected_count) + " accounts due to protection <br>" +
                    create_notification_log(error_log, 1, ERROR_LOG),
                ALERT_DANGER
            )
        else:
            set_notification(
                self.request,
                "Successfully deleted " + str(items_deleted_count) + " accounts <br>" +
                    create_notification_log(success_log, 1, SUCCESS_LOG),
                ALERT_SUCCESS
            )

            if len(error_log) > 0:
                set_notification(
                    self.request,
                    "Failed to delete " + str(items_protected_count) + " accounts due to protection<br>" +
                        create_notification_log(error_log, 2, ERROR_LOG),
                    ALERT_DANGER
                )

        return HttpResponseRedirect(reverse("account_manager.browse"))
