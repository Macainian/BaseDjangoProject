from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailAuthBackend(ModelBackend):
    """ Login by email and password """
    def authenticate(self, username=None, password=None, **kwargs):
        # Note that User.email is not unique, thus we can't use objects.get
        user = User.objects.filter(email__iexact=username, is_active=True).first()

        if user and user.check_password(password):
            return user

        return None


class CaseInsensitiveUsernameAuthBackend(ModelBackend):
    """ Make username case insensitive """
    def authenticate(self, username=None, password=None, **kwargs):
        users = User.objects.filter(username__iexact=username, is_active=True)

        for user in users:
            if user.check_password(password):
                return user

        return None
