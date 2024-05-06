from rest_framework import serializers
from api.models import *


class PredictInforSerializers(serializers.ModelSerializer):

    class Meta:
        model = PredictInfo
        fields = ['type_name_garbage', 'image_garbage', 'created_at']
