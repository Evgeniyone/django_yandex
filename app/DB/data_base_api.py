from datetime import datetime
from django.db.models import Q
from DB.models import Courier, ValueCourier, Order
from orders.order_definition import get_orders_id, cancel_orders


def add_courier_to_db(couriers):
    for courier in couriers:
        Courier(courier_id=courier['courier_id'],
                courier_type=courier["courier_type"],
                regions=courier['regions'],
                working_hours=courier['working_hours']).save()

        for region in courier['regions']:
            ValueCourier(courier_id=courier['courier_id'], region=region).save()


def add_orders_to_db(orders):
    for order in orders:
        Order(order_id=order['order_id'],
              weight=order["weight"],
              region=order['region'],
              delivery_hours=order['delivery_hours']).save()


def assign_update_courier_order(element, right_orders):
    query_ords = Q()
    for ord_id in right_orders:
        query_ords.add(Q(order_id=ord_id), Q.OR)
    temps = Order.objects.filter(query_ords).all()
    for temp in temps:
        temp.taken = True
        temp.save()
    element.orders = right_orders.__str__()
    element.last_assign_courier_type = element.courier_type
    element.assign_time = datetime.now()
    element.last_time = datetime.now()
    element.save()


def del_extra_orders(courier, orders_cor):
    query_ords = Q()
    for id in eval(orders_cor):
        query_ords.add(Q(order_id=id), Q.OR)
    orders_fields = Order.objects.filter(query_ords).all()

    a = eval(courier.orders)

    query_ords_cancel = Q()
    for order_id_del in cancel_orders([courier.courier_id, courier.courier_type, eval(courier.regions),
                                       eval(courier.working_hours)], orders_fields):
        a.remove(order_id_del)
        query_ords_cancel.add(Q(order_id=order_id_del),
                              Q.OR)
    temps = Order.objects.filter(query_ords_cancel).all()
    for temp in temps:
        temp.taken = False
        temp.save()

    courier.orders = a.__str__()
    courier.save()


def assign_give_orders(element):
    query = Q()
    for reg in eval(element.regions):
        query.add(Q(region=reg, taken=False), Q.OR)

    return get_orders_id([element.courier_id, element.courier_type, element.regions, eval(element.working_hours)],
                         Order.objects.filter(query).all())


def exist(courier_id):
    if Courier.objects.filter(courier_id=courier_id).exists():
        return True
    else:
        return False


def has_order(courier_id, order_id):
    mass_orders = Courier.objects.get(courier_id=courier_id).orders
    if len(eval(mass_orders)) != 0 and order_id in eval(mass_orders):
        return True
    return False


def complete_order_update_data(dict_json, id):
    element = Courier.objects.get(courier_id=dict_json['courier_id'])
    order = Order.objects.get(order_id=id)
    region = order.region
    order.delete()

    temp = ValueCourier.objects.get(courier_id=element.courier_id, region=region)

    act = datetime.strptime(dict_json['complete_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
    last = element.last_time

    last.replace(microsecond=int(round(last.microsecond / 1000000, 2) * 100))
    a = act - last

    temp.sum_time += a.total_seconds()
    temp.counts += 1
    temp.save()

    element.last_time = datetime.strptime(dict_json['complete_time'], "%Y-%m-%dT%H:%M:%S.%fZ")

    a = eval(element.orders)
    a.remove(id)
    element.orders = a.__str__()
    if len(a) == 0:
        C = {'foot': 2, 'bike': 5, 'car': 9}
        element.earnings += 500 * C[element.last_assign_courier_type]
    element.save()
