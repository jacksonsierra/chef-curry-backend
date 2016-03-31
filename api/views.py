from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
import json

from api.models import DeviceToken
from api.utils import calculate_state


@csrf_exempt
def register(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        try:
            token, created = DeviceToken.objects.get_or_create(token=body['device_token'])
        except DeviceToken.DoesNotExist:
            return HttpResponse(content=sys.exc_info()[0], status=500)

        if created:
            return HttpResponse(status=201)

        return HttpResponse(status=202)

    return HttpResponse(status=400)


def load_state(request):
    state = calculate_state(date=date.today())
    return HttpResponse(content=json.dumps({'type': state}), content_type='application/json')
