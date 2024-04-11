from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework import filters

import requests
import base64

from datetime import datetime

from django.conf import settings
import os

import numpy as np
from PIL import Image
from keras.models import load_model

from .serializers import PredictSerializer
from io import BytesIO

from api.models import *

ESP_IP = "172.20.10.7"

model = load_model(
    'C:/PBL5/SmartTrash/ai/model/fine_tunning_resnet50_model_custom_data_31_03.h5')


class ImageClassifierMVS(viewsets.ModelViewSet):
    prediction = None
    percent_predict = None

    serializer_class = PredictSerializer()

    @action(detail=False, methods=['POST'])
    def predict(self, request):
        serializer = PredictSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            img = Image.open(image)
            img = img.resize((384, 384))
            img_array = np.array(img)
            test_img = np.expand_dims(img_array, axis=0)

            prediction_prob = model.predict(test_img)
            print(prediction_prob)

            max_index = np.argmax(prediction_prob)
            print("Index of max value: ", max_index)
            max_value = prediction_prob[0][max_index]
            print("Max value: ", max_value)
            switcher = {
                0: 'Metal',
                1: 'paper',
                2: 'plastic',
            }
            prediction = switcher.get(max_index, 'Trash')

            percent_predict = max_value * 100
            response_data = {
                "message": "Dự đoán thành công !",
                "predict_result": prediction,
                "predict_percent": percent_predict,
            }

            return Response(data=response_data, status=status.HTTP_200_OK)
        return Response(
            data={
                'message': "Không dự đoán được Image .Vui lòng thử lại"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # @action(detail=False, methods=['GET'], url_path="get_image_from_esp32", url_name='get_image_from_esp32')
    # def get_image_from_esp32(self, request,  *args, **kwargs):
    #     # ESP_IP = "10.10.58.221"
    #     image_url = f"http://{ESP_IP}/cam-hi.jpg"
    #     # return Response(BytesIO(response.content), media_type="image/jpeg")
    #     try:
    #         response = requests.get(image_url)
    #         if response.status_code == 200:
    #             image = Image.open(BytesIO(response.content))
    #             buffered = BytesIO()
    #             image.save(buffered, format="JPEG")
    #             image_base64 = base64.b64encode(
    #                 buffered.getvalue()).decode('utf-8')
    #             return Response({'image_base64': image_base64}, status=status.HTTP_200_OK)
    #         else:
    #             return Response({'error': 'Failed to fetch image'}, status=response.status_code)
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], url_path="predict_image_from_esp32", url_name='predict_image_from_esp32')
    def predict_image_from_esp32(self, request,  *args, **kwargs):
        # serializer_class = PredictSerializer
        image_url = f"http://{ESP_IP}/cam-hi.jpg"
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                img = image.resize((384, 384))
                img_array = np.array(img)
                test_img = np.expand_dims(img_array, axis=0)

                current_time = datetime.now()
                timestamp = current_time.strftime("%d-%m-%Y_%H-%M-%S")
                image_filename = f"esp32_image_{timestamp}.jpg"

                image_path = os.path.join(
                    settings.MEDIA_ROOT, 'images', image_filename)
                img.save(image_path)

                prediction_prob = model.predict(test_img)
                print(prediction_prob)

                max_index = np.argmax(prediction_prob)
                print("Index of max value: ", max_index)
                max_value = prediction_prob[0][max_index]
                print("Max value: ", max_value)
                switcher = {
                    0: 'Metal',
                    1: 'paper',
                    2: 'plastic',
                }
                prediction = switcher.get(max_index, 'Trash')

                percent_predict = max_value * 100
                response_data = {
                    "message": "Dự đoán thành công !",
                    "predict_result": prediction,
                    "predict_percent": percent_predict,
                }
                return Response(data=response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], url_path="get_image_by_id_garbage_info", url_name='get_image_by_id_garbage_info')
    def get_image_by_id_garbage_info(self, request,  *args, **kwargs):
        try:
            id_garbage = kwargs['id']
            print("Giá trị của id là: ", id_garbage)
            if id_garbage == 0:
                return Response(data={}, status=status.HTTP_200_OK)

            garbage_info = GarbageInfo.objects.get(pk=id_garbage)

            if garbage_info.image_garbage_predict:
                image_url = request.build_absolute_uri(
                    garbage_info.image_garbage_predict.url)
                return Response(
                    data={
                        'image_url': image_url
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    data={
                        'error': 'Image not available'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as error:
            print("ImageClassifierMVS_get_image_by_id_garbage_info: ", error)
        return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
