from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('account/', include('api.account.urls')),
    path('model/', include('api.model.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
