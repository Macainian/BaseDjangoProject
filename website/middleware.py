import json
import sys
from re import compile

from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.urls import reverse

# Support for python 2 and 3
if sys.version_info > (3, 0):
    from urllib.parse import quote
else:
    from urllib import quote


class HttpRedirectException(Exception):
    def __init__(self, url, message=""):
        super(self.__class__, self).__init__()
        self.message = message
        self.url = url


class HttpResponseException(Exception):
    def __init__(self, response, status_code):
        super(self.__class__, self).__init__()
        self.response = response
        self.status_code = status_code


class RedirectionMiddleware(object):
    """ Redirect user if RedirectException is raised """
    @staticmethod
    def process_exception(request, exception):
        if isinstance(exception, HttpRedirectException):
            return HttpResponseRedirect(exception.url)

        # todo: Make this its own middleware instead of piggybacking off of this middleware
        if isinstance(exception, HttpResponseException):
            return HttpResponse(content=json.dumps(exception.response), status=exception.status_code)

        return None


# Alex black magic
LOGIN_EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip("/")), compile(settings.LOGOUT_URL.lstrip("/"))]
if hasattr(settings, "LOGIN_EXEMPT_URLS"):
    if isinstance(settings.LOGIN_EXEMPT_URLS, str):
        LOGIN_EXEMPT_URLS.append(compile(settings.LOGIN_EXEMPT_URLS))
    else:
        LOGIN_EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


# Alex black magic
STAFF_MEMBER_EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip("/")), compile(settings.LOGOUT_URL.lstrip("/"))]
if hasattr(settings, "STAFF_MEMBER_EXEMPT_URLS"):
    if isinstance(settings.STAFF_MEMBER_EXEMPT_URLS, str):
        STAFF_MEMBER_EXEMPT_URLS.append(compile(settings.STAFF_MEMBER_EXEMPT_URLS))
    else:
        STAFF_MEMBER_EXEMPT_URLS += [compile(expr) for expr in settings.STAFF_MEMBER_EXEMPT_URLS]


class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.

    Origin:
    http://stackoverflow.com/questions/3214589/django-how-can-i-apply-the-login-required-decorator-to-my-entire-site-excludin
    """
    def process_request(self, request):
        redirect_url = settings.LOGIN_URL + "?next=%s" % quote(request.build_absolute_uri())
        is_authenticated = request.user.is_authenticated() if hasattr(request, "user") else False  # Black magic
        path = request.path_info.lstrip("/")

        if not is_authenticated:
            if not any(m.match(path) for m in LOGIN_EXEMPT_URLS):
                print("Failed to match \"" + str(path) + "\" to " + str(LOGIN_EXEMPT_URLS))

                return HttpResponseRedirect(redirect_url)
        elif hasattr(request.user, "staff_member"):
            if request.user.staff_member.generated_password:
                if "auth" not in request.path_info.lstrip("/"):
                    return HttpResponseRedirect(reverse("website.staff_member_password_change"))
        else:
            # If is_authenticated by is not an Staff Member
            if not any(m.match(path) for m in STAFF_MEMBER_EXEMPT_URLS):
                print("Failed to match \"" + str(path) + "\" to " + str(STAFF_MEMBER_EXEMPT_URLS))

                raise PermissionDenied
