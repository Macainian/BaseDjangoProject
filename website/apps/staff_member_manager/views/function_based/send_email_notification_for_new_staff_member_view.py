from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from website.apps.staff_member_manager.models import StaffMember
from website.apps.staff_member_manager.utils.send_email_notification_for_new_staff_member import \
    send_email_notification_for_new_staff_member


@csrf_exempt
@login_required
def send_email_notification_for_new_staff_member_view(request, staff_member_id):
    staff_member = StaffMember.objects.get(id=staff_member_id)

    send_email_notification_for_new_staff_member(request, staff_member)

    return HttpResponse()
