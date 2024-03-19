from rest_framework import serializers


class PredictSerializer(serializers.Serializer):
    image = serializers.ImageField()

    class Meta:
        fields = ['image']
