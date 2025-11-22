from django.urls import path, include

# shared region view
from core.apps.shared.views import region as region_view
# shared district view
from core.apps.shared.views import district as dis_view


urlpatterns = [
    path('region/', include(
        [
            path('list/', region_view.RegionListApiView.as_view(), name='region-list-api'),
        ],
    )),
    path('disctrict/', include(
        [
            path('list/', dis_view.DistrictListApiView.as_view(), name='district-list-api'),
            path('create/', dis_view.DistrictCreateApiView.as_view(), name='district-create-api'),
        ],
    )),
]   