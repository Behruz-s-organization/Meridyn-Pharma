from django.urls import path, include

### dashboard ###
# users
from core.apps.dashboard.views import user as user_views


urlpatterns = [
    path('user/', include(
        [
            path('list/', user_views.UserListApiView.as_view(), name='user-list-api'),
        ],
    )),
]