from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from website.notification import set_notification, ALERT_SUCCESS


@login_required
def staff_member_password_change_done_view(request):
    # Reset generated_password if user is an StaffMember after they changed it
    if hasattr(request.user, "staff_member"):
        request.user.staff_member.generated_password = ""
        request.user.staff_member.save()

    set_notification(request, "Successfully changed the password", ALERT_SUCCESS)

    return HttpResponseRedirect(reverse("index"))
