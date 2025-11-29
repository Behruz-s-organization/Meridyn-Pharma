# django
from django.urls import path, include

# rest framework
from rest_framework.routers import DefaultRouter

### dashboard ###
# users
from core.apps.dashboard.views import user as user_views
# district
from core.apps.dashboard.views import district as district_views
# doctor
from core.apps.dashboard.views.doctor import DoctorViewSet
# region
from core.apps.dashboard.views import region as region_views
# plan 
from core.apps.dashboard.views.plan import PlanViewSet

urlpatterns = [
    # -------------- user -------------- 
    path('user/', include(
        [
            path('list/', user_views.UserListApiView.as_view(), name='user-list-api'),
            path('create/', user_views.UserCreateApiView.as_view(), name='user-create-api'),
            path('<int:id>/delete/', user_views.UserDeleteApiView.as_view(), name='user-delete-api'),
            path('<int:id>/update/', user_views.UserUpdateApiView.as_view(), name='user-update-api'),
            path('<int:id>/activate/', user_views.UserActivateApiView.as_view(), name='user-activate-api'),
        ],
    )),
    # -------------- district --------------
    path('district/', include(
        [
            path('list/', district_views.DistrictListApiView.as_view(), name='district-list-api'),
            path('create/', district_views.DistrictCreateApiView.as_view(), name='district-create-api'),
            path('<int:id>/update/', district_views.DistrictUpdateApiView.as_view(), name='district-update-api'),
            path('<int:id>/delete/', district_views.DistrictDeleteApiView.as_view(), name='district-delete-api'),
        ]
    )),
    # -------------- region --------------
    path('region/', include(
        [
            path('list/', region_views.RegionListApiView.as_view(), name='region-list-api'),
            path('create/', region_views.RegionCreateApiView.as_view(), name='region-create-api'),
            path('<int:id>/update/', region_views.RegionUpdateApiView.as_view(), name='region-update-api'),
            path('<int:id>/delete/', region_views.RegionDeleteApiView.as_view(), name='region-delete-api'),
        ]
    )),
]


### ViewSets ###
router = DefaultRouter()
router.register("doctor", DoctorViewSet)
router.register("plan", PlanViewSet)

urlpatterns += router.urls