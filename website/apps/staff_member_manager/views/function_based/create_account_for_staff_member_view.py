from django.http import HttpResponse

from website.apps.account_manager.utils.errors import AccountCreationError
from website.apps.staff_member_manager.models import StaffMember
from website.apps.staff_member_manager.utils.create_account_for_staff_member import create_account_for_staff_member


def create_account_for_staff_member_view(request, staff_member_id):
    staff_member = StaffMember.objects.get(id=staff_member_id)

    try:
        create_account_for_staff_member(staff_member)
    except AccountCreationError as error:
        return HttpResponse(content=str(error), status=500)

    return HttpResponse()
