from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django.db.models import Q
import requests
from django.conf import settings
import os
from django.db.models import Count

from .serializers import *


class PredictInforMVS(viewsets.ModelViewSet):
    serializer_class = PredictInforSerializers
    permission_classes = [IsAuthenticated]

    @action(methods=['GET'], detail=False, url_path="get_all_predict_infor_by_id_garbage_api", url_name="get_all_predict_infor_by_id_garbage_api")
    def get_all_predict_infor_by_id_garbage_api(self, request, *args, **kwargs):
        try:
            garbage_id = kwargs['id']
            if garbage_id == 0:
                return Response(data={}, status=status.HTTP_404_NOT_FOUND)
            queryset = PredictInfo.objects.filter(
                garbage_compartment__garbage_id=garbage_id).order_by('-created_at')
            serializer = self.serializer_class(queryset, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            print("PredictInforMVS_get_all_predict_infor_by_id_garbage_api: ", error)
        return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False, url_path="delete_all_predict_infor_by_id_compartment_api", url_name="delete_all_predict_infor_by_id_compartment_api")
    def delete_all_predict_infor_by_id_compartment_api(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                result = serializer.delete_predict(request)
                if result:
                    return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(
                "PredictInforMVS_delete_all_predict_infor_by_id_compartment_api: ", error)
        return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
