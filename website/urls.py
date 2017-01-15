from django.conf.urls import include, url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView

from django.contrib.auth import views

from website.views.function_based.login import login

urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),
    url(r"^$", TemplateView.as_view(template_name="index.html"), name="index"),
    url(r"^credits/$", TemplateView.as_view(template_name="credits.html"), name="credits"),
    # robots.txt is implemented as a template because Django can't seem to serve a static file from urls.py
    url(r"^robots.txt$", TemplateView.as_view(template_name="robots.txt")),

    url(r"^auth/login/$", login, name="login"),
    url(r"^auth/logout/$", views.logout, name="logout"),

    url(r"^auth/change_password/$", views.password_change, name="website.change_password",
        kwargs={"post_change_redirect": reverse_lazy("website.change_password_done")}),
    url(r"^auth/change_password_done/$", views.password_change_done, name="website.change_password_done"),

    # Using post_change_redirect to reset staff_member.generated_password after the first login
    # (in website.staff_member_password_change_done)
    # url(r"^auth/staff_member_password_change/$", views.password_change, name="website.staff_member_password_change",
    #     kwargs={"post_change_redirect": reverse_lazy("website.staff_member_password_change_done")}),
    # url(r"^auth/staff_member_password_change_done/$", staff_member_password_change_done_view,
    #     name="website.staff_member_password_change_done"),

    url(r"^password_reset/$", views.password_reset, name="password_reset"),
    url(r"^password_reset/done/$", views.password_reset_done, name="password_reset_done"),
    url(r"^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.password_reset_confirm, name="password_reset_confirm"),
    url(r"^reset/done/$", views.password_reset_complete, name="password_reset_complete"),

    # django-registration-redux URLs
    # https://django-registration-redux.readthedocs.org/en/latest/quickstart.html#setting-up-urls
    # url(r"^accounts/", include("registration.backends.default.urls")),

    # START APP URLS
    url(r"^address/", include("website.apps.address.urls")),
    url(r"^email_manager/", include("website.apps.email_manager.urls")),
    url(r"^staff_member_manager/", include("website.apps.staff_member_manager.urls")),
    url(r"^account_manager/", include("website.apps.account_manager.urls")),
    # END APP URLS
]

# handler404 = TemplateView.as_view(template_name="404.html")
