from rest_framework import serializers
from api.models import *


# class ProfileBasicSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['phone']


# class UserBasicSerializers(serializers.ModelSerializer):
#     # profile = ProfileBasicSerializers(required=False)
#     profile = serializers.SerializerMethodField(
#         method_name='get_profile_w_user')

#     def get_profile_w_user(self, instance):
#         queryset = instance.user_w_profile
#         if queryset:
#             return ProfileBasicSerializers(queryset).data
#         return None

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'profile']
class NotifyBasicSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notify
        fields = "__all__"


class GarbageBasicCompartment(serializers.ModelSerializer):

    class Meta:
        model = GarbageCompartment
        fields = ['type_name_compartment', 'distance_is_full']


class GarbageSerializers(serializers.ModelSerializer):
    # user = UserBasicSerializers(required=False)
    user_id = serializers.IntegerField(required=False)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Garbage
        fields = '__all__'

    def add(self, request):
        try:
            garbage_code = self.validated_data['garbage_code']
            name_country = self.validated_data['name_country']
            description = self.validated_data['description']
            user_id = self.validated_data['user_id']

            return Garbage.objects.create(user_id=user_id, garbage_code=garbage_code,
                                          name_country=name_country, description=description)
        except Exception as error:
            print("GarbageSerializers_add_error: ", error)
            return None

    def delete(self, request):
        try:
            model = Garbage.objects.get(pk=self.validated_data['id'])
            model.delete()
            return True
        except Exception as error:
            print("GarbageSerializer_delete_error: ", error)
            return False

    def update(self, request):
        try:
            garbage_id = self.validated_data['id']
            user_id = self.validated_data['user_id']
            garbage_code = self.validated_data['garbage_code']
            name_country = self.validated_data['name_country']
            description = self.validated_data['description']
            #
            garbage = Garbage.objects.get(pk=garbage_id)
            #
            garbage.user_id = user_id
            garbage.garbage_code = garbage_code
            garbage.description = description
            garbage.name_country = name_country
            garbage.save()
            #
            return garbage
        except Exception as error:
            print("GarbageSerializers_update_error: ", error)
            return None


# class PredictInforSerializers(serializers.ModelSerializer):

#     class Meta:
#         model = PredictInfo
#         field = "__all__"
