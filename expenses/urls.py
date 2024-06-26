from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.landing, name="landing"),
    path('initiate_payment/', views.initiate_payment, name='initiate_payment'),
    path('process_payment/<int:payment_id>/', views.process_payment, name='process_payment'),
    # path('send-email/', views.send_email_view, name='send_email'),
    path('add_common_expense/', views.add_common_expense, name='add_common_expense'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path("cash_payment/", views.cash_payment, name="cash_payment"),
 


]
