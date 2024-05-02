from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.core.validators import EmailValidator
from api.models import *


def getUserFromAccessToken(self, access_token):
    try:
        access_token = AccessToken(access_token)
        user_id = access_token["user_id"]
        user = User.objects.get(pk=user_id)
        return user
    except:
        return None


class AccountRegisterSerializers(serializers.ModelSerializer):
    phone = serializers.CharField(required=True, allow_blank=False)
    confirm_password = serializers.CharField(required=True, allow_blank=False)
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            "email": {"validators": [EmailValidator]},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {"message": "Incorrect password and confirm_password confirmation."}
            )
        else:
            return data

    def username_validate(self):
        try:
            user = User.objects.get(username=self.validated_data["username"])
            return False
        except User.DoesNotExist:
            return True

    def add(self, request):
        try:
            username = self.validated_data['username']
            phone = self.validated_data['phone']
            email = self.validated_data['email']
            password = self.validated_data['password']
            # confirm_password = self.validated_data['confirm_password']
            user = User()
            user.username = username
            user.email = email
            user.password = make_password(password)
            user.save()
            #
            Profile.objects.create(user=user, phone=phone)
            return True
        except Exception as error:
            print("AccountSerializers_add_error: ", error)
            return False


class AccountLoginSerializers(serializers.ModelSerializer):
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, data):
        username = data['username']
        password = data['password']
        if username and password:
            user = User.objects.filter(username=username).first()
            if user and user.check_password(password):
                return data
        raise serializers.ValidationError(
            {"message": "Incorrect username or password."}
        )

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


class ResetPasswordSerializers(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, allow_blank=False)
    new_password = serializers.CharField(required=True, allow_blank=False)
    confirm_new_password = serializers.CharField(
        required=True, allow_blank=False)
    id = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ['id', 'old_password', 'new_password', 'confirm_new_password']

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError(
                {"message": "Incorrect new password and password confirmation."}
            )
        else:
            return data

    def old_password_validate(self):
        user = User.objects.get(pk=self.validated_data["id"])
        if not user.check_password(self.validated_data["old_password"]):
            return False
        return True

    def update(self):
        try:
            new_password = self.validated_data['new_password']
            id = self.validated_data['id']
            user = User.objects.get(pk=id)
            if user:
                user.set_password(new_password)
                user.save()
            return user
        except Exception as error:
            print("AccountSerializers_reset_password_error: ", error)
            return None
