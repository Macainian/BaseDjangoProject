from django.conf.urls import url

from website.apps.staff_member_manager.views.class_based.BrowseView import BrowseView
from website.apps.staff_member_manager.views.class_based.DeleteView import DeleteView
from website.apps.staff_member_manager.views.class_based.DetailsView import DetailsView
from website.apps.staff_member_manager.views.class_based.EditView import EditView
from website.apps.staff_member_manager.views.function_based.create_account_for_staff_member_view import \
    create_account_for_staff_member_view
from website.apps.staff_member_manager.views.function_based.send_email_notification_for_new_staff_member_view import \
    send_email_notification_for_new_staff_member_view
from website.apps.staff_member_manager.views.function_based.set_is_active_view import set_is_active_view
from website.apps.staff_member_manager.views.function_based.set_is_staff_view import set_is_staff_view
from website.apps.staff_member_manager.views.function_based.set_is_superuser_view import set_is_superuser_view

urlpatterns = [
    url(r"^browse/$", BrowseView.as_view(), name="staff_member_manager.browse"),
    url(r"^edit/(?P<staff_member_id>.*)/$", EditView.as_view(), name="staff_member_manager.edit"),
    url(r"^delete", DeleteView.as_view(), name="staff_member_manager.delete"),
    url(r"^details/(?P<staff_member_id>.*)/$", DetailsView.as_view(), name="staff_member_manager.details"),

    url(r"^set_is_active/$", set_is_active_view, name="staff_member_manager.set_is_active"),
    url(r"^set_is_staff/$", set_is_staff_view, name="staff_member_manager.set_is_staff"),
    url(r"^set_is_superuser/$", set_is_superuser_view, name="staff_member_manager.set_is_superuser"),

    url(r"^send_email_notification_for_new_staff_member/(?P<staff_member_id>\w+)/$",
        send_email_notification_for_new_staff_member_view,
        name="staff_member_manager.send_email_notification_for_new_staff_member"),

    url(r"^create_account_for_staff_member/(?P<staff_member_id>\w+)/$", create_account_for_staff_member_view,
        name="staff_member_manager.create_account_for_staff_member"),
]
