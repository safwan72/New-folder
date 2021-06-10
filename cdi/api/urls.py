from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('models', ModelListAPIView.as_view(), name='model_info'),
    path('models/user/', model_list, name='model_info_user'),
    path('company', ActiveCompanyAPIView.as_view(), name='company_info'),
]
