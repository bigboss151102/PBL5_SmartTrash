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
from django.db.models import Avg, F, Subquery, OuterRef

from .serializers import *
# from api.pagination import *


class GarbageMVS(viewsets.ModelViewSet):
    serializer_class = GarbageSerializers
    # permission_classes = [IsAuthenticated]

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


class GarbageCompartmentMVS(viewsets.ModelViewSet):

    serializer_class = GarbageBasicCompartment
    permission_classes = [IsAuthenticated]

    @action(methods=['GET'], detail=False, url_path="get_distance_is_full_compartment_by_id_api", url_name="get_distance_is_full_compartment_by_id_api")
    def get_distance_is_full_compartment_by_id_api(self, request, *args, **kwargs):
        try:
            garbage_id = kwargs['id']
            if garbage_id == 0:
                return Response(data={}, status=status.HTTP_404_NOT_FOUND)
            queryset = GarbageCompartment.objects.filter(garbage_id=garbage_id)
            serializer = self.serializer_class(queryset, many=True)
            # print(serializer.data)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            print(
                "GarbageCompartmentMVS_get_distance_is_full_compartment_by_id_api: ", error)
        return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False, url_path="get_average_garbage_quantity_by_compartment_api", url_name="get_average_garbage_quantity_by_compartment_api")
    def get_average_garbage_quantity_by_compartment_api(self, request, *args, **kwargs):
        try:
            # Khởi tạo danh sách để lưu trữ thông tin của mỗi name_country
            data_list = []

            # Subquery để lấy các giá trị duy nhất của name_country từ Garbage
            subquery = Garbage.objects.filter(
                id=OuterRef('garbage_id')).values('name_country')

            # Tính số lượng bản ghi trong PredictInfo cho mỗi GarbageCompartment
            compartment_counts = PredictInfo.objects.values(
                'garbage_compartment').annotate(count=Count('id'))

            # Lấy tất cả các bản ghi của GarbageCompartment cùng với số lượng đếm từ PredictInfo
            garbage_compartments = GarbageCompartment.objects.all().annotate(
                garbage_count=Subquery(
                    compartment_counts.filter(
                        garbage_compartment=OuterRef('id')).values('count')
                )
            )

            # Câu truy vấn chính để tính giá trị trung bình của số lượng rác cho mỗi loại ngăn (Metal, Plastic, Paper)
            average_quantities = garbage_compartments.values('garbage__name_country', 'type_name_compartment').annotate(
                avg_quantity=Avg('garbage_count')
            )

            # Lặp qua kết quả của truy vấn và gán giá trị trung bình vào danh sách data_list
            for compartment in average_quantities:
                name_country = compartment['garbage__name_country']
                compartment_type = compartment['type_name_compartment']
                avg_quantity = compartment['avg_quantity']

                # Tìm hoặc tạo mới một entry cho name_country trong data_list
                found = False
                for data in data_list:
                    if data["name_country"] == name_country:
                        found = True
                        data["value_average"][compartment_type] = avg_quantity
                        break

                # Nếu name_country chưa tồn tại trong data_list, tạo mới một entry cho nó
                if not found:
                    data_list.append({
                        "name_country": name_country,
                        "value_average": {
                            "Metal": 0,
                            "Plastic": 0,
                            "Paper": 0,
                            "Another": 0
                        }
                    })
                    data_list[-1]["value_average"][compartment_type] = avg_quantity

            return Response(data=data_list, status=status.HTTP_200_OK)
        except Exception as error:
            print("Error:", error)
            return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


class NotifyMVS(viewsets.ModelViewSet):

    @action(methods=['GET'], detail=False, url_path="get_all_notify_api", url_name="get_all_notify_api")
    def get_all_notify_api(self, request, *args, **kwargs):
        try:
            data = {}
            garbage_compartments = GarbageCompartment.objects.all()
            if garbage_compartments.exists():
                for compartent in garbage_compartments:
                    count = PredictInfo.objects.filter(
                        garbage_compartment=compartent).count()
                    if count > 5:
                        message = f"Ngăn {compartent.type_name_compartment} đã đầy"
                        notify = Notify.objects.create(
                            message=message, garbage=compartent.garbage)

            notifications = Notify.objects.all()
            if notifications.exists():
                for notify in notifications:
                    data['message'] = notify.message
                    data['garbage_code'] = notify.garbage.garbage_code if notify.garbage else "Unknown",
                    data['created_at'] = notify.garbage.created_at
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as error:
            print("NotifyMVS_get_all_notify: ", error)
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
