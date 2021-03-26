from django.urls import path
from orders import views

urlpatterns = [
    path('', views.post_orders),
    path('/assign', views.assign),
    path('/complete', views.complete),
]
