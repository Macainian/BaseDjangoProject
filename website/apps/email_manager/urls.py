from django.conf.urls import url

from website.apps.email_manager.views.class_based.BrowseView import BrowseView
from website.apps.email_manager.views.class_based.EmailBatchTemplateEditorView import EmailBatchTemplateEditorView
from website.apps.email_manager.views.function_based.email_batch_template_views import get_email_batch_template_view, \
    save_email_batch_template_view, copy_email_batch_template_view, get_email_preview_view


urlpatterns = [
    url(r"^browse/$", BrowseView.as_view(), name="email_manager.browse"),
    # url(r"^edit/(?P<email_id>.*)/$", EditView.as_view(), name="email_manager.edit"),
    # url(r"^delete/$", DeleteView.as_view(), name="email_manager.delete"),

    url(r"email_batch_template_editor/$", EmailBatchTemplateEditorView.as_view(),
        name="email_manager.email_batch_template_editor"),
    url(r"^get_email_preview/$", get_email_preview_view, name="email_manager.get_email_preview"),

    url(r"^get_email_batch_template/(?P<email_batch_template_id>\w+)/$", get_email_batch_template_view,
        name="email_manager.get_email_batch_template"),
    url(r"^save_email_batch_template/(?P<email_batch_template_id>\w+)/$", save_email_batch_template_view,
        name="email_manager.save_email_batch_template"),
    url(r"^copy_email_batch_template/(?P<email_batch_template_id>\w+)/$", copy_email_batch_template_view,
        name="email_manager.copy_email_batch_template"),
]
