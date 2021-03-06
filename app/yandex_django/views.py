import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from DB.models import Courier, ValueCourier, Order


@csrf_exempt
def clear_db(request):
    if 'pass' in str(request.body) \
            and json.loads(request.body)['pass'] == '/dev/null':
        Courier.objects.all().delete()
        ValueCourier.objects.all().delete()
        Order.objects.all().delete()
        return JsonResponse({'status':'OK'}, status=200)
    return JsonResponse("", status=404, safe=False)
