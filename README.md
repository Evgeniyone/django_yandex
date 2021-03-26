# django_yandex
Django REST API сервис, который позволяет нанимать курьеров на работу,
принимать заказы и оптимально распределять заказы между курьерами, попутно считая их рейтинг и заработок.
### Инструкция развёртывания:
1. Установить [Docker](https://docs.docker.com/get-docker/)
2. Если Linux установить [Docker-Compose](https://docs.docker.com/compose/install/)
3. Клонировать репозиторий, перейти в корень.
4. Для запуска сервера выполнить команду `docker-compose up -d --build`.
### Реализованные методы:
1. POST /couriers
2. PATCH /couriers/$courier_id
3. POST /orders
4. POST /orders/assign
5. POST /orders/complete
6. GET /couriers/$courier_id<br>
Документация методов [openapi.yaml](openapi.yaml)<br>
### Тестирование
При запуске сервера выполняются тесты из [tests.py](/app/yandex_django/tests.py)<br>
Запуск тестов описан в [entrypoint.sh](/app/entrypoint.sh)
