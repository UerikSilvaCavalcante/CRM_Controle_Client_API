from django.urls import path
from auth_user.views import *


urlpatterns = [
    path("login/", CustomAuthToken.as_view(), name="login"),
    path("login_cliente/", CustomClienteAuthToken.as_view(), name="login_cliente"),
]
