from django.urls import path, include

### dashboard ###
# users
from core.apps.dashboard.views import user as user_views


urlpatterns = [
    path('user/', include(
        [
            path('list/', user_views.UserListApiView.as_view(), name='user-list-api'),
            path('create/', user_views.UserCreateApiView.as_view(), name='user-create-api'),
            path('<int:id>/delete/', user_views.UserDeleteApiView.as_view(), name='user-delete-api'),
            path('<int:id>/update/', user_views.UserUpdateApiView.as_view(), name='user-update-api'),
        ],
    )),
]