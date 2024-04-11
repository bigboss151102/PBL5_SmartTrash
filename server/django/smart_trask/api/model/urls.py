from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import ImageClassifierMVS

predict_image = ImageClassifierMVS.as_view({
    'post': 'predict'
})

get_image_from_esp32 = ImageClassifierMVS.as_view({
    'get': 'get_image_from_esp32'
})

predict_image_from_esp32 = ImageClassifierMVS.as_view({
    'get': 'predict_image_from_esp32'
})

get_image_by_id_garbage_info = ImageClassifierMVS.as_view({
    'get': 'get_image_by_id_garbage_info'
})

urlpatterns = [
    path('predict-image/', predict_image, name='predict-image'),
    path('get_image_from_esp32/', get_image_from_esp32),
    path('predict_image_from_esp32/', predict_image_from_esp32),
    path('get_image_by_id_garbage_info/<int:id>', get_image_by_id_garbage_info),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
