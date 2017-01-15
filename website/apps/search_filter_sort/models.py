from django.db import models
from django.conf import settings

MODELS_MODULE_PATH = settings.APPS_SEARCH_FILTER_SORT_MODELS_MODULE_PATH

# Anywhere you see default=None, this is being used to force integrity error if this is not supplied on creation


