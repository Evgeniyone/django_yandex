import json
from django.http import JsonResponse
from cerberus import Validator
from django.views.decorators.csrf import csrf_exempt

from DB.data_base_api import assign_give_orders, complete_order_update_data, exist, has_order, \
    assign_update_courier_order, add_orders_to_db
from DB.models import Courier, Order
from orders.models import OrdersPostRequest, OrderItemSchema, OrdersAssignPostRequest, \
    OrdersCompletePostRequest


@csrf_exempt
def post_orders(request):
    if request.method == 'POST':
        validator = Validator()
        if validator.validate(json.loads(request.body), OrdersPostRequest):
            print(json.loads(request.body)['data'][0])

            order_val = True
            err = {}
            for order in json.loads(request.body)['data']:
                if not validator.validate(order, OrderItemSchema):
                    err[order['order_id']] = validator.errors
                    order_val = False
                elif Order.objects.filter(order_id=order['order_id']).exists():
                    err[order['order_id']] = "already exists"
                    order_val = False

            if order_val:
                add_orders_to_db(json.loads(request.body)['data'])

                id_for_json = [{"id": x['order_id']} for x in json.loads(request.body)['data']]
                return JsonResponse({'orders': id_for_json}, status=201)
            else:
                print([{"id": order, "additionalProp1": err[order]} for order in err])
                return JsonResponse(
                    {"validation_error": {"orders": [{"id": order, "error": err[order]} for order in err], }},
                    status=400)
        else:
            return JsonResponse(
                {"validation_error": {"orders": [{"id": 0}], "additionalProp1": {"error": validator.errors}}},
                status=400)
    return


@csrf_exempt
def assign(request):
    if request.method == 'POST':
        validator = Validator()
        dict_json = json.loads(request.body)
        if validator.validate(dict_json, OrdersAssignPostRequest) and exist(
                dict_json['courier_id']):
            id_for_json = []

            el = Courier.objects.get(
                courier_id=dict_json['courier_id'])
            if len(eval(el.orders)) == 0:

                right_orders = assign_give_orders(el)

                if len(right_orders) != 0:
                    assign_update_courier_order(el, right_orders)
                else:
                    return JsonResponse({'orders': [{"id": id} for id in
                                                    id_for_json]})
            id_for_json = eval(el.orders)
            assign_time = el.assign_time

            return JsonResponse({'orders': [{"id": id} for id in id_for_json],
                                 'assign_time': assign_time.
                                strftime('%Y-%m-%dT%H:%M:%S.%f')[:-4] + 'Z'})
    return JsonResponse("", status=400, safe=False)


@csrf_exempt
def complete(request):
    if request.method == 'POST':
        validator = Validator()
        dict_json = json.loads(request.body)
        id = dict_json['order_id']
        if validator.validate(dict_json, OrdersCompletePostRequest) and exist(dict_json['courier_id']) \
                and has_order(dict_json['courier_id'], dict_json['order_id']):
            complete_order_update_data(dict_json, id)

            return JsonResponse({"order_id": id})
        else:
            return JsonResponse("", status=400, safe=False)
    return
