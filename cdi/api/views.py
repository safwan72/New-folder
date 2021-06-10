from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
from cdi.models import ActiveAdminModel, ActiveCompany
from blogger.models import User
import json
from .serializers import *


class ModelListAPIView(ListAPIView):
    queryset = ActiveAdminModel.objects.all()
    serializer_class = ActiveModelListSerializer


@api_view(["POST"])
def model_list(request):
    try:
        payload = json.loads(request.body)
        user = User.objects.get(id=payload['id'], _id_slug=payload['_id_slug'])
        print(user)
        if user.admin:
            queryset = list(ActiveAdminModel.objects.all().values())
        else:
            queryset = list(ActiveAdminModel.objects.filter(admin=False).values())

        return JsonResponse(
            queryset,
            safe=False,
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return JsonResponse(
            {'error': 'Something terrible went wrong, ' + str(e)},
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class ActiveCompanyAPIView(ListAPIView):
    queryset = ActiveCompany.objects.all()
    serializer_class = ActivecompanyListSerializer
