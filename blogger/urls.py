from django.contrib import admin
from django.urls import path, include
from .views import dashboard, confirm_setup_account

urlpatterns = [
    path('', dashboard, name="blogdi_dashboard"),
    path('confirm-setup', confirm_setup_account, name='confirm_setup_account')
]
