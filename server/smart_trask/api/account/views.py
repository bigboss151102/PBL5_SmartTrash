from .serializers import *
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.db.models import Q, Count
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
import re


class AccountMVS(viewsets.ModelViewSet):
    serializer_class = AccountSerializers

    @action(methods=["POST"], detail=False, url_path="account_register_add_api", url_name="account_register_add_api")
    def account_register_add_api(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            data = {}
            if serializer.is_valid():
                model = serializer.add(request)
                if model:
                    data['message'] = 'Add successfully!'
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    data['message'] = 'Passwords are not the same !'
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            data['message'] = "Username is exist !"
            return Response(
                data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("AccountMVS_account_register_add_api: ", error)
        return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["POST"], detail=False, url_path="account_login_api", url_name="account_login_api")
    def account_login_api(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            data = {}
            if serializer.is_valid():
                model = serializer.login(request)
                if model:
                    refresh = RefreshToken.for_user(model)
                    access_token = refresh.access_token
                    data['token'] = str(access_token)
                    return Response(data, status=status.HTTP_200_OK)
            data['message'] = "Please check username or password"
            return Response(
                data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("AccountMVS_account_login_api: ", error)
        return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
