from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from website.models import BaseModel

MODELS_MODULE_PATH = settings.APPS_ADDRESS_MODELS_MODULE_PATH

# Anywhere you see default=None, this is being used to force integrity error if this is not supplied on creation


class Country(models.Model):
    name = models.TextField(unique=True, default=None, editable=False)
    country_code = models.TextField(null=True, blank=True, editable=False)

    class Meta:
        db_table = "country"
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name

    @staticmethod
    def basic_search_list():
        return ["name", "country_code"]

    @staticmethod
    def special_search_list():
        return []

    @staticmethod
    def object_dependencies():
        return []


class State(models.Model):
    # Name is the native version of the name
    name = models.TextField(default=None, editable=False)
    # Simple name is the name without special characters outside of the standard 26 English alphabet
    simple_name = models.TextField(default=None, editable=False)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.PROTECT, editable=False)
    state_code = models.TextField(null=True, blank=True, editable=False)
    type = models.TextField(default=None, editable=False)

    class Meta:
        db_table = "state"
        verbose_name = "State"
        verbose_name_plural = "States"

    def __str__(self):
        return self.name

    @staticmethod
    def basic_search_list():
        return ["name", "simple_name", "state_code", "type"]

    @staticmethod
    def special_search_list():
        return []

    @staticmethod
    def object_dependencies():
        return [("country", MODELS_MODULE_PATH, "Country")]


class City(models.Model):
    # Name is the native version of the name
    name = models.TextField(default=None, editable=False)
    # Simple name is the name without special characters outside of the standard 26 English alphabet
    simple_name = models.TextField(default=None, editable=False)
    state = models.ForeignKey(State, null=True, blank=True, on_delete=models.PROTECT, editable=False)
    city_code = models.TextField(null=True, blank=True, editable=False)
    lat_long = models.TextField(null=True, blank=True, editable=False)

    class Meta:
        db_table = "city"
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name

    @staticmethod
    def basic_search_list():
        return ["name", "simple_name", "city_code", "lat_long"]

    @staticmethod
    def special_search_list():
        return []

    @staticmethod
    def object_dependencies():
        return [("state", MODELS_MODULE_PATH, "State")]


class Address(BaseModel):
    street_address = models.TextField(null=True, blank=True)
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.PROTECT)
    state = models.ForeignKey(State, null=True, blank=True, on_delete=models.PROTECT)
    zip_code = models.TextField(null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.PROTECT)

    created_by = models.ForeignKey(User, related_name="created_addresses", on_delete=models.PROTECT)
    updated_by = models.ForeignKey(User, related_name="updated_addresses", on_delete=models.PROTECT)

    class Meta:
        db_table = "address"
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        if self.street_address is not None:
            street_address = self.street_address + ", "
        else:
            street_address = ""

        if self.city is not None:
            city_name = self.city.name + ", "
        else:
            city_name = ""

        if self.state is not None:
            state_name = self.state.name + " "
        else:
            state_name = ""

        if self.zip_code is not None:
            zip_code = self.zip_code + ", "
        else:
            zip_code = ""

        if self.country is not None:
            country_name = self.country.name
        else:
            country_name = ""

        return street_address + city_name + state_name + zip_code + country_name

    @staticmethod
    def basic_search_list():
        return ["street_address", "zip_code"]

    @staticmethod
    def special_search_list():
        return []

    @staticmethod
    def object_dependencies():
        return [
            ("city", MODELS_MODULE_PATH, "City"), ("state", MODELS_MODULE_PATH, "State"),
            ("country", MODELS_MODULE_PATH, "Country"),
            ("created_by", settings.APPS_STAFF_MEMBER_MANAGER_MODELS_MODULE_PATH, "StaffMember"),
            ("updated_by", settings.APPS_STAFF_MEMBER_MANAGER_MODELS_MODULE_PATH, "StaffMember"),
        ]

    def copy(self):
        address = Address.objects.create(
            country=self.country, zip_code=self.zip_code, state=self.state, city=self.city,
            street_address=self.street_address
        )

        return address
