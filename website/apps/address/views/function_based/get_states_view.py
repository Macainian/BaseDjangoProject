import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from website.other_apps.address.models import State


@csrf_exempt
@login_required
def get_states_view(request, country_id):
    states = State.objects.filter(country_id=country_id).order_by("simple_name")

    if len(states) == 0:
        return HttpResponse(content=json.dumps({}))

    state_info_list = [(state.id, state.simple_name) for state in states]

    data = {}
    data["state_info_list"] = state_info_list
    data["state_type"] = states[0].type

    return HttpResponse(content=json.dumps(data))
