from rest_framework import serializers
from api.models import *


class PredictSerializer(serializers.Serializer):
    image = serializers.ImageField()
    id_garbage = serializers.IntegerField(required=False)

    class Meta:
        fields = ['image']

    # def get_image_by_id_garbage_info(self, request):
    #     id_garbage = self.validated_data['id_garbage']

    #     garbage_info = GarbageInfo.objects.get(pk = id_garbage)

