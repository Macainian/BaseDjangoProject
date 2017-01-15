from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from website.apps.address.models import Address
from website.apps.staff_member_manager.models import StaffMember
from website.models import BaseModel


MODELS_MODULE_PATH = settings.APPS_ACCOUNT_MANAGER_MODELS_MODULE_PATH

# Anywhere you see default=None, this is being used to force integrity error if this is not supplied on creation


class AccountType(BaseModel):
    name = models.TextField(unique=True, default=None)

    created_by = models.ForeignKey(StaffMember, related_name="created_account_types", on_delete=models.PROTECT)
    updated_by = models.ForeignKey(StaffMember, related_name="updated_account_types", on_delete=models.PROTECT)

    class Meta:
        app_label = "account_manager"
        db_table = "account_type"
        verbose_name = "Account Type"
        verbose_name_plural = "Account Types"

    def __str__(self):
        return self.name

    @staticmethod
    def basic_search_list():
        return ["name"]

    @staticmethod
    def special_search_list():
        return []

    @staticmethod
    def object_dependencies():
        return [
            ("created_by", settings.APPS_STAFF_MEMBER_MANAGER_MODELS_MODULE_PATH, "StaffMember"),
            ("updated_by", settings.APPS_STAFF_MEMBER_MANAGER_MODELS_MODULE_PATH, "StaffMember"),
        ]


class Account(models.Model):
    user = models.OneToOneField(User)
    user_token = models.TextField(null=True, blank=True)
    type = models.ForeignKey(AccountType, on_delete=models.PROTECT)

    email_is_confirmed = models.BooleanField(default=False)
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        db_table = "account"
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.user.username

    @staticmethod
    def basic_search_list():
        return [
        ]

    @staticmethod
    def special_search_list():
        return []

    @staticmethod
    def object_dependencies():
        return [
            ("type", MODELS_MODULE_PATH, "AccountType"),
            ("address", settings.APPS_ADDRESS_MODELS_MODULE_PATH, "Address"),
        ]
