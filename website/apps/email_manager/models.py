from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from website.apps.staff_member_manager.models import StaffMember
from website.models import BaseModel, UniqueCode

MODELS_MODULE_PATH = settings.APPS_EMAIL_MANAGER_MODELS_MODULE_PATH

# Anywhere you see default=None, this is being used to force integrity error if this is not supplied on creation


class EmailBatchType(BaseModel):
    name = models.TextField(unique=True, default=None)

    created_by = models.ForeignKey(StaffMember, related_name="created_email_batch_types", on_delete=models.PROTECT)
    updated_by = models.ForeignKey(StaffMember, related_name="updated_email_batch_types", on_delete=models.PROTECT)

    class Meta:
        db_table = "email_batch_type"
        verbose_name = "Email Batch Type"
        verbose_name_plural = "Email Batch Types"

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


class EmailBatchStatus(BaseModel):
    name = models.TextField(unique=True, default=None)

    created_by = models.ForeignKey(StaffMember, related_name="created_email_batch_statuses", on_delete=models.PROTECT)
    updated_by = models.ForeignKey(StaffMember, related_name="updated_email_batch_statuses", on_delete=models.PROTECT)

    class Meta:
        db_table = "email_batch_status"
        verbose_name = "Email Batch Status"
        verbose_name_plural = "Email Batch Statuses"

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


class EmailBatchTemplate(BaseModel):
    name = models.TextField(unique=True, default=None)
    from_code = models.TextField(default=None)
    subject_code = models.TextField(default=None)
    basic_message = models.TextField(default=None)  # This is used if the email doesn't accept html
    html_code = models.TextField(default=None)

    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(StaffMember, related_name="created_email_batch_templates", on_delete=models.PROTECT)
    updated_by = models.ForeignKey(StaffMember, related_name="updated_email_batch_templates", on_delete=models.PROTECT)

    class Meta:
        db_table = "email_batch_template"
        verbose_name = "Email Batch Template"
        verbose_name_plural = "Email Batch Templates"

    def __str__(self):
        return self.name

    @staticmethod
    def basic_search_list():
        return ["name", "from_code", "subject_code", "basic_message", "html_code"]

    @staticmethod
    def special_search_list():
        return []

    @staticmethod
    def object_dependencies():
        return [
            ("created_by", settings.APPS_STAFF_MEMBER_MANAGER_MODELS_MODULE_PATH, "StaffMember"),
            ("updated_by", settings.APPS_STAFF_MEMBER_MANAGER_MODELS_MODULE_PATH, "StaffMember"),
        ]


class EmailBatch(BaseModel):
    type = models.ForeignKey(EmailBatchType, on_delete=models.PROTECT)
    status = models.ForeignKey(EmailBatchStatus, on_delete=models.PROTECT)
    template = models.ForeignKey(EmailBatchTemplate, on_delete=models.PROTECT)

    created_by = models.ForeignKey(StaffMember, related_name="created_email_batches", on_delete=models.PROTECT)
    updated_by = models.ForeignKey(StaffMember, related_name="updated_email_batches", on_delete=models.PROTECT)

    class Meta:
        db_table = "email_batch"
        verbose_name = "Email Batch"
        verbose_name_plural = "Email Batches"

    def __str__(self):
        return self.creation_datetime

    @staticmethod
    def basic_search_list():
        return []

    @staticmethod
    def special_search_list():
        return []

    @staticmethod
    def object_dependencies():
        return [
            ("type", MODELS_MODULE_PATH, "EmailBatchType"),
            ("status", MODELS_MODULE_PATH, "EmailBatchStatus"),
            ("template", MODELS_MODULE_PATH, "EmailBatchTemplate"),
            ("created_by", settings.APPS_STAFF_MEMBER_MANAGER_MODELS_MODULE_PATH, "StaffMember"),
            ("updated_by", settings.APPS_STAFF_MEMBER_MANAGER_MODELS_MODULE_PATH, "StaffMember"),
        ]


class EmailInstanceStatus(BaseModel):
    name = models.TextField(unique=True, default=None)

    created_by = models.ForeignKey(StaffMember, related_name="created_email_instance_statuses", on_delete=models.PROTECT)
    updated_by = models.ForeignKey(StaffMember, related_name="updated_email_instance_statuses", on_delete=models.PROTECT)

    class Meta:
        db_table = "email_instance_status"
        verbose_name = "Email Instance Status"
        verbose_name_plural = "Email Instance Statuses"

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


class EmailInstance(BaseModel):
    batch = models.ForeignKey(EmailBatch, related_name="email_instances", on_delete=models.PROTECT)
    recipient_email = models.TextField(default=None)
    status = models.ForeignKey(EmailInstanceStatus, on_delete=models.PROTECT)

    created_by = models.ForeignKey(StaffMember, related_name="created_email_instances", on_delete=models.PROTECT)
    updated_by = models.ForeignKey(StaffMember, related_name="updated_email_instances", on_delete=models.PROTECT)
    sent_datetime = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "email_instance"
        verbose_name = "Email Instance"
        verbose_name_plural = "Email Instances"

    def __str__(self):
        return self.creation_datetime

    @staticmethod
    def basic_search_list():
        return ["recipient_email"]

    @staticmethod
    def special_search_list():
        return []

    @staticmethod
    def object_dependencies():
        return [
            ("batch", MODELS_MODULE_PATH, "EmailBatch"),
            ("status", MODELS_MODULE_PATH, "EmailInstanceStatus"),
            ("created_by", settings.APPS_STAFF_MEMBER_MANAGER_MODELS_MODULE_PATH, "StaffMember"),
            ("updated_by", settings.APPS_STAFF_MEMBER_MANAGER_MODELS_MODULE_PATH, "StaffMember"),
        ]


class DoNotSendEmailList(BaseModel):
    name = models.TextField(unique=True, default=None)

    created_by = models.ForeignKey(StaffMember, related_name="created_do_not_send_email_lists", on_delete=models.PROTECT)
    updated_by = models.ForeignKey(StaffMember, related_name="updated_do_not_send_email_lists", on_delete=models.PROTECT)

    class Meta:
        db_table = "do_not_send_email_list"
        verbose_name = "Do Not Send Email List"
        verbose_name_plural = "Do Not Send Email Lists"

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


class DoNotSendEmailListItem(BaseModel):
    email = models.TextField(unique=True, default=None)

    list = models.ForeignKey(DoNotSendEmailList, related_name="email_items", on_delete=models.PROTECT)

    created_by = models.ForeignKey(StaffMember, related_name="created_do_not_send_email_list_items", on_delete=models.PROTECT)
    updated_by = models.ForeignKey(StaffMember, related_name="updated_do_not_send_email_list_items", on_delete=models.PROTECT)

    class Meta:
        db_table = "do_not_send_email_list_item"
        verbose_name = "Do Not Send Email List Item"
        verbose_name_plural = "Do Not Send Email List Items"

    def __str__(self):
        return self.email

    @staticmethod
    def basic_search_list():
        return ["email"]

    @staticmethod
    def special_search_list():
        return []

    @staticmethod
    def object_dependencies():
        return [
            ("list", MODELS_MODULE_PATH, "DoNotSendEmailList"),
            ("created_by", settings.APPS_STAFF_MEMBER_MANAGER_MODELS_MODULE_PATH, "StaffMember"),
            ("updated_by", settings.APPS_STAFF_MEMBER_MANAGER_MODELS_MODULE_PATH, "StaffMember"),
        ]


class PasswordResetCode(UniqueCode):
    email_instance = models.ForeignKey(EmailInstance, on_delete=models.PROTECT)
    creation_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "password_reset_code"
        verbose_name = "Password Reset Code"
        verbose_name_plural = "Password Reset Codes"

    def __str__(self):
        return self.id

    @property
    def type(self):
        return self.email_instance.batch.type

    @property
    def recipient_email(self):
        return self.email_instance.recipient_email

    @staticmethod
    def basic_search_list():
        return []

    @staticmethod
    def special_search_list():
        return []

    @staticmethod
    def object_dependencies():
        return [
            ("email_instance", settings.APPS_EMAIL_MANAGER_MODELS_MODULE_PATH, "EmailInstance"),
        ]
