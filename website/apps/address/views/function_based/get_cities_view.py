import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from website.other_apps.address.models import City


@csrf_exempt
@login_required
def get_cities_view(request, state_id):
    cities = City.objects.filter(state_id=state_id).order_by("simple_name")

    if len(cities) == 0:
        return HttpResponse(content=json.dumps({}))

    city_info_list = [(city.id, city.simple_name) for city in cities]

    return HttpResponse(content=json.dumps(city_info_list))
