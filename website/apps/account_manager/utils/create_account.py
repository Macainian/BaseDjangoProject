from django.contrib.auth.models import User
from django.db import transaction

from website.apps.account_manager.models import Account


@transaction.atomic
def create_account(username, password, first_name, last_name, email, account_type):
    user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email)
    user.set_password(password)
    user.save()

    account = Account.objects.create(user=user, type=account_type)

    return account
