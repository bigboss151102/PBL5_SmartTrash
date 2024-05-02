from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

account_register_add_api = AccountRegisterMVS.as_view({
    'post': 'account_register_add_api'
})

account_login_api = AccountLoginMVS.as_view({
    'post': 'account_login_api'
})

account_reset_password_api = AccountResetPasswordMVS.as_view({
    'post': 'account_reset_password_api'
})


urlpatterns = [
    path('account_register_add_api/', account_register_add_api),
    path('account_login_api/', account_login_api),
    path('account_reset_password_api/', account_reset_password_api),
    path('model/', include('api.model.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
