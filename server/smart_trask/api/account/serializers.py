from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from api.models import *


class AccountSerializers(serializers.ModelSerializer):
    phone = serializers.CharField(required=False, allow_blank=True)
    repeat_password = serializers.CharField(required=False, allow_blank=True)
    username = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = '__all__'

    def add(self, request):
        try:
            username = self.validated_data['username']
            phone = self.validated_data['phone']
            email = self.validated_data['email']
            password = self.validated_data['password']
            repeat_password = self.validated_data['repeat_password']
            print(password)
            print(repeat_password)
            if str(password) == str(repeat_password):
                user = User()
                user.username = username
                user.email = email
                user.password = make_password(password)
                user.save()
                #
                Profile.objects.create(user=user, phone=phone)
                return True
            return False
        except Exception as error:
            print("AccountSerializers_add_error: ", error)
            return None

    def login(self, request):
        try:
            username = self.validated_data['username']
            password = self.validated_data['password']
            user = User.objects.filter(username=username).first()
            if user and user.check_password(password):
                return user
            return None
        except Exception as error:
            print("AccountSerializers_login_error: ", error)
            return None
