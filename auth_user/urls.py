from django.urls import path
from auth_user.views import *


urlpatterns = [
    path("login/", CustomAuthToken.as_view(), name="login"),
]
