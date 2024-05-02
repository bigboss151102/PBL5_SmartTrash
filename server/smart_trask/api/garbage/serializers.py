from rest_framework import serializers
from api.models import *


class GarbageSerializers(serializers.ModelSerializer):
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
