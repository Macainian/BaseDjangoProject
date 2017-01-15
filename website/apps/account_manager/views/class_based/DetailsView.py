from django.views.generic import TemplateView

from website.apps.account_manager.models import Account
from website.mixins import LoginRequiredMixin


class DetailsView(LoginRequiredMixin, TemplateView):
    template_name = "account_manager/details.html"

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)

        account_id = kwargs["account_id"]
        account = Account.objects.get(id=account_id)
        context["account"] = account

        return context
