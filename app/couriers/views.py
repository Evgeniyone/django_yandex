import json
from cerberus import Validator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist, Q

from DB.models import Courier, ValueCourier, Order
from DB.data_base_api import add_courier_to_db, del_extra_orders

from .models import CouriersPostRequest, CourierItem, CourierUpdateRequest


@csrf_exempt
def index(request):
    if request.method == 'POST':

        validator = Validator()
        if validator.validate(json.loads(request.body), CouriersPostRequest):
            dict_json = json.loads(request.body)
            order_val = True
            err = {}
            for courier in dict_json['data']:
                if not validator.validate(courier, CourierItem):
                    err[courier['courier_id']] = validator.errors
                    order_val = False
                elif Courier.objects.filter(courier_id=courier['courier_id']).exists():
                    err[courier['courier_id']] = "already exists"
                    order_val = False
            if order_val:
                id_for_json = [{"id": x['courier_id']} for x in dict_json['data']]

                add_courier_to_db(dict_json['data'])

                return JsonResponse({"couriers": id_for_json}, status=201)

            else:
                return JsonResponse(
                    {"validation_error": {"couriers": [{"id": order, "error": err[order]} for order in err], }},
                    status=400)
        else:
            return JsonResponse({"validation_error": {"couriers": [{"id": 0}], "errors": {"error": validator.errors}}},
                                status=400)


@csrf_exempt
def getCourier(request, id):
    if request.method == 'GET':
        try:
            courier = Courier.objects.get(courier_id=id)

            earnings = courier.earnings

            jsn = {'courier_id': courier.courier_id, 'courier_type': courier.courier_type, 'regions': courier.regions,

                   'working_hours': courier.working_hours,
                   'earnings': earnings
                   }

            temp = ValueCourier.objects.filter(courier_id=id).all()
            if courier.earnings != 0:
                print("value", [i.sum_time / i.counts for i in temp if i.counts != 0])
                a = min([i.sum_time / i.counts for i in temp if i.counts != 0])
                jsn['rating'] = (60 * 60 - min(a, 60 * 60)) / (60 * 60) * 5

            return JsonResponse(jsn)
        except ObjectDoesNotExist:
            return JsonResponse("", status=404, safe=False)

    if request.method == 'PATCH':
        try:
            temp = json.loads(request.body)
            if Validator().validate(temp, CourierUpdateRequest):
                courier = Courier.objects.get(courier_id=id)
                if 'courier_type' in temp:
                    courier.courier_type = temp['courier_type']
                if 'regions' in temp:
                    courier.regions = temp['regions'].__str__()
                if 'working_hours' in temp:
                    courier.working_hours = temp['working_hours'].__str__()

                if len(eval(courier.orders)) != 0:
                    del_extra_orders(courier, courier.orders)

                courier.save()
                return JsonResponse({'courier_id': courier.courier_id})
            else:
                return JsonResponse("", status=400, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse("", status=404, safe=False)
