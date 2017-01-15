from django.conf import settings as django_settings

from website import global_definitions


def app_env(request):
    """ This function defines login and logout pages.
    If we are running in production enviroment, use auth_pubtkt.
    In dev enviroment, use local django auth system
    """
    env = {"LOGIN_URL": django_settings.LOGIN_URL,
           "REDIRECT_FIELD_NAME": getattr(django_settings, "REDIRECT_FIELD_NAME", "next"),
           "LOGOUT_URL": django_settings.LOGOUT_URL}
    # if hasattr(settings, "SERVER_MAINTENANCE_MESSAGE"):
    #      env["SERVER_MAINTENANCE_MESSAGE"] = settings.SERVER_MAINTENANCE_MESSAGE

    return env


def settings(request):
    """ This context processor injects django settings to the template
    """
    return {"SETTINGS": django_settings, "GLOBAL_DEFINITIONS": global_definitions}
