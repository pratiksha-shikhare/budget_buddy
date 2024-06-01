from django.urls import path
from . import views

urlpatterns = [
    path('initiate_payment/', views.initiate_payment, name='initiate_payment'),
    path('process_payment/<int:payment_id>/', views.process_payment, name='process_payment'),
]
