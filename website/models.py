import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db import transaction
from django.conf import settings


MODELS_MODULE_PATH = settings.WEBSITE_MODELS_MODULE_PATH

# Anywhere you see default=None, this is being used to force integrity error if this is not supplied on creation


class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)  # Not set directly. See the save() function.

    creation_datetime = models.DateTimeField(auto_now_add=True)
    last_modified_datetime = models.DateTimeField(auto_now=True)
    deletion_datetime = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.deletion_datetime:
            self.is_deleted = True

        super(BaseModel, self).save(*args, **kwargs)


class UniqueCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_expired = models.BooleanField(default=False)

    expiration_datetime = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.expiration_datetime:
            self.is_expired = True

        super(UniqueCode, self).save(*args, **kwargs)
