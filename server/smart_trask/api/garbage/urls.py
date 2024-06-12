from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

add_garbage_api = GarbageMVS.as_view({
    'post': 'add_garbage_api'
})

garbage_edit_api = GarbageMVS.as_view({
    'patch': "garbage_edit_api"
})

garbage_delete_api = GarbageMVS.as_view({
    'delete': 'garbage_delete_api'
})

garbage_get_all_by_user_api = GarbageMVS.as_view({
    'get': 'garbage_get_all_by_user_api'
})

get_quantity_compartment_by_id_api = GarbageMVS.as_view({
    'get': 'get_quantity_compartment_by_id_api'
})

# get_all_predict_infor_by_id_garbage_api = PredictInforMVS.as_view({
#     'get': 'get_all_predict_infor_by_id_garbage_api'
# })

get_distance_is_full_compartment_by_id_api = GarbageCompartmentMVS.as_view({
    'get': "get_distance_is_full_compartment_by_id_api"
})

get_average_garbage_quantity_by_compartment_api = GarbageCompartmentMVS.as_view({
    'get': 'get_average_garbage_quantity_by_compartment_api'
})

get_all_notify_api_by_user = NotifyMVS.as_view({
    'get': 'get_all_notify_api_by_user'
})
get_distance_from_ultrasonic_sensor = SensorUltraMVS.as_view({
    'get': 'get_distance_from_ultrasonic_sensor'
})
urlpatterns = [
    path('add_garbage_api/', add_garbage_api),
    path('garbage_edit_api/', garbage_edit_api),
    path('garbage_delete_api/', garbage_delete_api),
    path('garbage_get_all_by_user_api/', garbage_get_all_by_user_api),
    #
    path('get_quantity_compartment_by_id_api/<int:id>/',
         get_quantity_compartment_by_id_api),
    path('get_distance_is_full_compartment_by_id_api/<int:id>/',
         get_distance_is_full_compartment_by_id_api),
    path('get_average_garbage_quantity_by_compartment_api/',
         get_average_garbage_quantity_by_compartment_api),
    # path('get_all_predict_infor_by_id_garbage_api/<int:id>',
    #      get_all_predict_infor_by_id_garbage_api),
    #
    path('get_distance_from_ultrasonic_sensor/',
         get_distance_from_ultrasonic_sensor),
    path('get_all_notify_api_by_user/', get_all_notify_api_by_user),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
