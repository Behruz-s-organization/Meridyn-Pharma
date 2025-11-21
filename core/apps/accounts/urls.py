from django.urls import path, include

from core.apps.accounts.views import user as user_views

urlpatterns = [
    path('user/', include(
        [
            path('create', user_views.RegisterUserApiView.as_view(), name='user-register-api'),
        ],
    )),
]