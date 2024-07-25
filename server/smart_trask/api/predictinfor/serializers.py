from rest_framework import serializers
from api.models import *


class PredictInforSerializers(serializers.ModelSerializer):

    id_compartment = serializers.IntegerField(required=False)

    class Meta:
        model = PredictInfo
        fields = ['id_compartment', 'type_name_garbage',
                  'image_garbage', 'created_at']

    def delete_predict(self, request):
        try:
            compartment_id = self.validated_data['id_compartment']
            print(compartment_id)
            model = PredictInfo.objects.filter(
                garbage_compartment_id=compartment_id)
            model.delete()
            return True
        except Exception as error:
            print("PredictInforSerializers_delete_predict: ", error)
            return False
