import logging

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from website.apps.staff_member_manager.models import StaffMember

logger = logging.getLogger(__name__)


@csrf_exempt
@login_required
def set_is_active_view(request):
    other_staff_member_username = request.POST["other_staff_member_username"]
    is_checked = request.POST["is_checked"]

    if is_checked == "true":
        is_checked = True
    elif is_checked == "false":
        is_checked = False
    else:
        return HttpResponse(content="is_checked is not true nor false", status=500)

    if other_staff_member_username == "admin" or other_staff_member_username == "Macainian":
        return HttpResponse(content=other_staff_member_username + " is not allowed to be changed", status=500)

    other_staff_member = StaffMember.objects.get(user__username=other_staff_member_username)

    if is_checked:
        other_staff_member.user.is_active = True
    else:
        other_staff_member.user.is_active = False

    other_staff_member.user.save()

    return HttpResponse()
