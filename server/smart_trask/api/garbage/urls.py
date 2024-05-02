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


urlpatterns = [
    path('add_garbage_api/', add_garbage_api),
    path('garbage_edit_api/', garbage_edit_api),
    path('garbage_delete_api/', garbage_delete_api),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
