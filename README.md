# django_yandex
Django REST API сервис, который позволяет нанимать курьеров на работу,
принимать заказы и оптимально распределять заказы между курьерами, попутно считая их рейтинг и заработок.
### Инструкция развёртывания:
1. Установить [Docker](https://docs.docker.com/get-docker/)
2. Если Linux установить [Docker-Compose](https://docs.docker.com/compose/install/)
3. Для запуска сервера выполнить команду `docker-compose up -d --build` из директории django_yandex.
### Тестирование
При запуске сервера выполняются тесты из [tests.py](/app/yandex_django/tests.py)<br>
Запуск тестов описан в [entrypoint.sh](/app/entrypoint.sh)
