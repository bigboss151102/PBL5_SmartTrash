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
from api import status_http
import re


class AccountRegisterMVS(viewsets.ModelViewSet):
    serializer_class = AccountRegisterSerializers

    @action(methods=["POST"], detail=False, url_path="account_register_add_api", url_name="account_register_add_api")
    def account_register_add_api(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            data = {}
            if serializer.is_valid():
                bool_temp = serializer.username_validate()
                print(bool_temp)
                if not serializer.username_validate():
                    data['message'] = 'Username is exist !'
                    return Response(data, status=status_http.HTTP_ME_450_USERNAME_EXIST)
                model = serializer.add(request)
                if model:
                    data['message'] = 'Add successfully!'
                    return Response(data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("AccountMVS_account_register_add_api: ", error)
        return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


class AccountLoginMVS(viewsets.ModelViewSet):
    serializer_class = AccountLoginSerializers

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
                # data['message'] = "Please check username or password"
                # return Response(
                #     data, status=status.HTTP_400_BAD_REQUEST)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("AccountMVS_account_login_api: ", error)
        return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


class AccountResetPasswordMVS(viewsets.ModelViewSet):
    serializer_class = ResetPasswordSerializers
    permission_classes = [IsAuthenticated]

    @action(methods=["POST"], detail=False, url_path="account_reset_password_api", url_name="account_reset_password_api")
    def account_reset_password_api(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            data = {}
            if serializer.is_valid():
                if not serializer.old_password_validate():
                    data['message'] = 'Old password is incorrect'
                    return Response(data, status=status_http.HTTP_ME_454_OLD_PASSWORD_IS_INCORRECT)
                model = serializer.update()
                if model:
                    data['message'] = "Reset Password Sucessfully"
                    return Response(data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("ResetPasswordMVS_account_reset_password_api: ", error)
        return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
