from datetime import datetime

OrderItemSchema = {
    'order_id': {'type': 'integer',
                 'required': True,
                 'min': 1
                 },
    'weight': {'type': 'float',
               'required': True,
               'min': 0.01,
               'max': 50.0
               },
    'region': {'type': 'integer',
               'required': True,
               'min': 1
               },
    'delivery_hours': {'type': 'list',
                       'schema': {
                           'type': 'string',
                           'regex': '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]-([0-1]?[0-9]|2[0-3]):[0-5][0-9]',
                           'required': True
                       },

                       'required': True
                       }
}

OrdersPostRequest = {
    'data': {
        'type': 'list',
        'required': True
    },
}
OrdersAssignPostRequest = {
    'courier_id': {
        'type': 'integer',
        'required': True
    }
}


def is_less_now(field, value, error):
    if not value.date() < datetime.utcnow().date():
        error(field, "time is more now")
        print("time is more now")


A = {
    'type': 'datetime',
    'coerce': lambda s: datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ')
}
B = {
    'type': 'integer',
    'min': 1,
    'max': 10000000000
}

OrdersCompletePostRequest = {
    'courier_id': {
        'type': 'integer'
    },
    'order_id': {
        'type': 'integer'
    },
    'complete_time': {
        'type': 'string',
        'anyof_schema': [A, B]


    },

}
