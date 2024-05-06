from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.db.models import Q
import requests
from django.conf import settings
import os
from django.db.models import Count

from .serializers import *
# from api.pagination import *


class GarbageMVS(viewsets.ModelViewSet):
    serializer_class = GarbageSerializers
    permission_classes = [IsAuthenticated]

    @action(methods=['POST'], detail=False, url_path="add_garbage_api", url_name="add_garbage_api")
    def add_garbage_api(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                model = serializer.add(request)
                if model:
                    data = {}
                    data['message'] = "Add successfully"
                    return Response(data=data, status=status.HTTP_201_CREATED)
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("GarbageMVS_add_api: ", error)
        return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=False,  url_path="garbage_delete_api", url_name="garbage_delete_api")
    def garbage_delete_api(self, request, *arg, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = {}
                result = serializer.delete(request)
                if result:
                    data['message'] = 'Delete successfully!'
                    return Response(data=data, status=status.HTTP_204_NO_CONTENT)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("GarbageMVS_delete_api: ", error)
        return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PATCH'], detail=False,  url_path="garbage_edit_api", url_name="garbage_edit_api")
    def garbage_edit_api(self, request, *arg, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                model = serializer.update(request)
                if model:
                    data = {}
                    data['message'] = 'Update successfully!'
                    return Response(data=data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("GarbageMVS_edit_api: ", error)
        return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False, url_path="garbage_get_all_by_user_api", url_name="garbage_get_all_by_user_api")
    def garbage_get_all_by_user_api(self, request, *args, **kwargs):
        user_id = request.user.id
        if user_id == 0:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)
        query = Q(user__id=user_id)
        queryset = Garbage.objects.filter(
            query).order_by('created_at').distinct()
        serializer = self.serializer_class(
            queryset, many=True, context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path="get_quantity_compartment_by_id_api", url_name="get_quantity_compartment_by_id_api")
    def get_quantity_compartment_by_id_api(self, request, *args, **kwargs):
        try:
            garbage_id = kwargs['id']
            if garbage_id == 0:
                return Response(data={}, status=status.HTTP_404_NOT_FOUND)
            data = {
                'total_metal': 0,
                'total_plastic': 0,
                'total_paper': 0,
                'total_another': 0
            }
            compartments = GarbageCompartment.objects.filter(
                garbage_id=garbage_id)
            for compartment in compartments:
                compartment_id = compartment.id
                compartment_type = compartment.type_name_compartment
                num_garbage_count = PredictInfo.objects.filter(
                    garbage_compartment_id=compartment_id).count()
                if compartment_type == 'Metal':
                    data['total_metal'] += num_garbage_count
                elif compartment_type == 'Plastic':
                    data['total_plastic'] += num_garbage_count
                elif compartment_type == 'Paper':
                    data['total_paper'] += num_garbage_count
                elif compartment_type == 'Another':
                    data['total_another'] += num_garbage_count
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as error:
            print("GarbageMVS_get_quantity_compartment_by_id_api: ", error)
        return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


# class PredictInforMVS(viewsets.ModelViewSet):
#     serializer_class = PredictInforSerializers
#     permission_classes = [IsAuthenticated]
#     pagination_class = PredictInforPagination

#     @action(methods=['GET'], detail=False, url_path="get_all_predict_infor_by_id_garbage_api", url_name="get_all_predict_infor_by_id_garbage_api")
#     def get_all_predict_infor_by_id_garbage_api(self, request, *args, **kwargs):
#         try:
#             garbage_id = kwargs['id']
#             if garbage_id == 0:
#                 return Response(data={}, status=status.HTTP_404_NOT_FOUND)
#             queryset = PredictInfo.objects.filter(garbage_compartment__garbage_id =garbage_id)
#             serializer = self.serializer_class(queryset, many = True)
#             return Response(data = serializer.data, status= status.HTTP_200_OK)
#         except Exception as error:
#             print("PredictInforMVS_get_all_predict_infor_by_id_garbage_api: ", error)
#         return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
