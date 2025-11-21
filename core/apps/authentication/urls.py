from django.urls import path

from core.apps.authentication.views import login


urlpatterns = [
    path('login/', login.LoginApiView.as_view(), name='login-api'),
]