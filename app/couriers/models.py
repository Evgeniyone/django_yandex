CourierItem = {
    'courier_id': {'type': 'integer',
                   'required': True,
                   'min': 1
                   },
    'courier_type': {'type': 'string',
                     'required': True,
                     'allowed': ['foot', 'bike', 'car']
                     },
    'regions': {'type': 'list',
                'schema': {'type': 'integer',
                           'required': True
                           },
                'required': True,
                'min': 1
                },

    'working_hours': {'type': 'list',
                      'schema': {'type': 'string',
                                 'regex': '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]-([0-1]?[0-9]|2[0-3]):[0-5][0-9]',
                                 'required': True
                                 },

                      'required': True
                      }
}

CouriersPostRequest = {
    'data': {
        'type': 'list',
        'required': True
    },
}

CourierUpdateRequest = {
    'courier_type': {'type': 'string',
                     'allowed': ['foot', 'bike', 'car']
                     },
    'regions': {'type': 'list',
                'schema': {'type': 'integer',
                           'required': True
                           },
                },

    'working_hours': {'type': 'list',
                      'schema': {'type': 'string',
                                 'regex': '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]-([0-1]?[0-9]|2[0-3]):[0-5][0-9]',
                                 'required': True
                                 },
                      }
}
