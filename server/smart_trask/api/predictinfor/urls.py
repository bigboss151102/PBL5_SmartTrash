from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

get_all_predict_infor_by_id_garbage_api = PredictInforMVS.as_view({
    'get': 'get_all_predict_infor_by_id_garbage_api'
})


urlpatterns = [
    path('get_all_predict_infor_by_id_garbage_api/<int:id>/',
         get_all_predict_infor_by_id_garbage_api),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
