from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

MODELS_MODULE_PATH = settings.APPS_STAFF_MEMBER_MANAGER_MODELS_MODULE_PATH

# Anywhere you see default=None, this is being used to force integrity error if this is not supplied on creation


def make_random_password():
    return User.objects.make_random_password()


class StaffMember(models.Model):
    user = models.OneToOneField(User, related_name="staff_member")
    generated_password = models.TextField(blank=True, default=make_random_password)

    created_by = models.ForeignKey("self", null=True, blank=True, related_name="created_staff_members",
                                   on_delete=models.PROTECT)
    updated_by = models.ForeignKey("self", null=True, blank=True, related_name="updated_staff_members",
                                   on_delete=models.PROTECT)

    class Meta:
        default_related_name = "staff_member"
        db_table = "staff_member"
        verbose_name = "Staff Member"
        verbose_name_plural = "Staff Members"

    def __str__(self):
        return self.user.username

    @staticmethod
    def basic_search_list():
        return []

    @staticmethod
    def special_search_list():
        return []

    @staticmethod
    def object_dependencies():
        return [
            ("created_by", settings.APPS_STAFF_MEMBER_MANAGER_MODELS_MODULE_PATH, "StaffMember"),
            ("updated_by", settings.APPS_STAFF_MEMBER_MANAGER_MODELS_MODULE_PATH, "StaffMember"),
        ]
