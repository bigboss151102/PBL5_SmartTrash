from django.urls import path
from .views import *

account_register_add_api = AccountMVS.as_view({
    'post': 'account_register_add_api'
})

account_login_api = AccountMVS.as_view({
    'post': 'account_login_api'
})

urlpatterns = [
    path('account_register_add_api/', account_register_add_api),
    path('account_login_api/', account_login_api),
]
