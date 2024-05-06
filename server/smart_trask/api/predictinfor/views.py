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


# class PredictInforPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 10
#     page_query_param = 'p'

#     def get_paginated_response(self, data):
#         next_page = previous_page = None
#         if self.page.has_next():
#             next_page = self.page.next_page_number()
#         if self.page.has_previous():
#             previous_page = self.page.previous_page_number()
#         return Response({
#             'totalRows': self.page.paginator.count,
#             'page_size': self.page_size,
#             'current_page': self.page.number,
#             'next_page': next_page,
#             'previous_page': previous_page,
#             'links': {
#                 'next': self.get_next_link(),
#                 'previous': self.get_previous_link(),
#             },
#             'data': data,
#         })


class PredictInforMVS(viewsets.ModelViewSet):
    serializer_class = PredictInforSerializers
    # pagination_class = PredictInforPagination
    permission_classes = [IsAuthenticated]

    @action(methods=['GET'], detail=False, url_path="get_all_predict_infor_by_id_garbage_api", url_name="get_all_predict_infor_by_id_garbage_api")
    def get_all_predict_infor_by_id_garbage_api(self, request, *args, **kwargs):
        try:
            garbage_id = kwargs['id']
            if garbage_id == 0:
                return Response(data={}, status=status.HTTP_404_NOT_FOUND)
            queryset = PredictInfo.objects.filter(
                garbage_compartment__garbage_id=garbage_id)
            # page = self.paginate_queryset(queryset)
            # if page is not None:
            #     serializer = self.get_serializer(page, many=True)
            #     return self.get_paginated_response(serializer.data)
            serializer = self.serializer_class(queryset, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            print("PredictInforMVS_get_all_predict_infor_by_id_garbage_api: ", error)
        return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
