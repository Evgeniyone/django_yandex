from django import test


class URLTests(test.TestCase):
    def setUp(self):
        data = {
            "data": [
                {
                    "courier_id": 3,
                    "courier_type": "car",
                    "regions": [
                        1
                    ],
                    "working_hours": [
                        "06:00-22:00"
                    ]
                },
                {
                    "courier_id": 4,
                    "courier_type": "foot",
                    "regions": [
                        45
                    ],
                    "working_hours": [
                        "06:00-13:00"
                    ]
                }
            ]
        }
        response = self.client.post('/couriers', data, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_couriers_get_right(self):
        response = self.client.get('/couriers/4')
        self.assertEqual(response.status_code, 200)

    def test_couriers_get_wrong(self):
        response = self.client.get('/couriers/5')
        self.assertEqual(response.status_code, 404)

    def test_couriers_patch_right(self):
        data = {
            "regions": [100, 200, 300]
        }
        response = self.client.patch('/couriers/4', data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_couriers_patch_wrong(self):
        data = {
            "regions": [100, 200, 300]
        }
        response = self.client.patch('/couriers/5', data, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_orders_post_right(self):
        data = {
            "data": [
                {
                    "order_id": 1,
                    "weight": 0.24,
                    "region": 12,
                    "delivery_hours": ["09:00-18:00"]
                },
                {
                    "order_id": 2,
                    "weight": 13,
                    "region": 1,
                    "delivery_hours": ["09:00-18:00"]
                },
                {
                    "order_id": 3,
                    "weight": 0.01,
                    "region": 22,
                    "delivery_hours": ["09:00-12:00", "16:00-21:30"]
                }
            ]
        }
        response = self.client.post('/orders', data, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_orders_post_wrong(self):
        data = {
            "data": [
                {
                    "order_id": 1,
                    "weight": 0.23,
                    "region": 12,
                    "delivery_hours": ["09:99-18:00"]
                },
                {
                    "order_id": 2,
                    "weight": 15,
                    "region": 1,
                    "delivery_hours": ["09:00-18:00"]
                },
                {
                    "order_id": 3,
                    "weight": 0.01,
                    "region": 22,
                    "delivery_hours": ["09:00-112:00", "16:00-21:30"]
                }
            ]
        }
        response = self.client.post('/orders', data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_orders_assign_post_right(self):
        data = {
            "courier_id": 3
        }
        response = self.client.post('/orders/assign', data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_orders_assign_post_wrong(self):
        data = {
            "courier_id": 2
        }
        response = self.client.post('/orders/assign', data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_orders_complete_post_right(self):
        data = {
            "data": [
                {
                    "order_id": 1,
                    "weight": 0.23,
                    "region": 12,
                    "delivery_hours": ["09:00-18:00"]
                },
                {
                    "order_id": 2,
                    "weight": 15,
                    "region": 1,
                    "delivery_hours": ["09:00-18:00"]
                },
                {
                    "order_id": 3,
                    "weight": 0.01,
                    "region": 1,
                    "delivery_hours": ["09:00-12:00", "16:00-21:30"]
                }
            ]
        }
        response = self.client.post('/orders', data, content_type='application/json')

        data = {
            "courier_id": 3
        }
        response = self.client.post('/orders/assign', data, content_type='application/json')

        data = {
            "courier_id": 3,
            "order_id": 3,
            "complete_time": "2021-01-10T10:33:01.42Z"
        }
        response = self.client.post('/orders/complete', data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_orders_complete_post_wrong(self):
        data = {
            "courier_id": 2,
            "order_id": 33,
            "complete_time": "2021-01-10T10:33:01.42Z"
        }
        response = self.client.post('/orders/assign', data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
