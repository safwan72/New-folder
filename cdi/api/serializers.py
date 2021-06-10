from rest_framework import serializers
from cdi.models import ActiveAdminModel, ActiveCompany


class ActiveModelListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActiveAdminModel
        exclude = ['id']


class ActivecompanyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActiveCompany
        exclude = ['id']
