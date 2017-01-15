from website.apps.account_manager.models import Account, AccountType
from website.apps.account_manager.utils.errors import AccountCreationError


def create_account_for_staff_member(staff_member):
    if Account.objects.filter(user__id=staff_member.user.id).exists():
        raise AccountCreationError("Staff Member already has an account")
    else:
    # Get Account Type
        account_types = AccountType.objects.all()

        if len(account_types) == 0:
            raise AccountCreationError("No Account Types in the system")

        account_type = account_types[0]

        Account.objects.create(user=staff_member.user, type=account_type)
