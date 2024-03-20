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

ESP_IP = "10.10.59.173"

model = load_model(
    'C:/PBL5/SmartTrash/ai/model/fine_tunning_resnet50_model.h5')


class ImageClassifier(viewsets.ModelViewSet):
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
                0: 'Cardboard',
                1: 'Glass',
                2: 'Metal',
                3: 'Paper',
                4: 'Plastic',
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

    @action(detail=False, methods=['GET'], url_path="get_image_from_esp32", url_name='get_image_from_esp32')
    def get_image_from_esp32(self, request,  *args, **kwargs):
        # ESP_IP = "10.10.58.221"
        image_url = f"http://{ESP_IP}/cam-hi.jpg"
        # return Response(BytesIO(response.content), media_type="image/jpeg")
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                buffered = BytesIO()
                image.save(buffered, format="JPEG")
                image_base64 = base64.b64encode(
                    buffered.getvalue()).decode('utf-8')
                return Response({'image_base64': image_base64}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to fetch image'}, status=response.status_code)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], url_path="predict_image_from_esp32", url_name='predict_image_from_esp32')
    def predict_image_from_esp32(self, request,  *args, **kwargs):
        # ESP_IP = "10.10.58.221"
        serializer_class = PredictSerializer
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
                print(max_index)
                max_value = prediction_prob[0][max_index]
                print(max_value)
                switcher = {
                    0: 'Cardboard',
                    1: 'Glass',
                    2: 'Metal',
                    3: 'Paper',
                    4: 'Plastic',
                }
                prediction = switcher.get(max_index, 'Trash')

                percent_predict = max_value * 100
                # if prediction_prob.any():
                #     if (prediction_prob[0][1] * 100) >= 90:
                #         prediction = "Glass"
                #         percent_predict = prediction_prob[0][1] * 100
                #     elif (prediction_prob[0][2] * 100) >= 90:
                #         prediction = "Metal"
                #         percent_predict = prediction_prob[0][2] * 100
                #     elif (prediction_prob[0][4] * 100) >= 90:
                #         prediction = "Plastic"
                #         percent_predict = prediction_prob[0][4] * 100
                #     else:
                #         prediction = "Loại rác khác"
                #         percent_predict = 0
                response_data = {
                    "message": "Dự đoán thành công !",
                    "predict_result": prediction,
                    "predict_percent": percent_predict,
                }
                return Response(data=response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
