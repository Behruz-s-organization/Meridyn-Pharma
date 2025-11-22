from django.urls import path, include

# shared region view
from core.apps.shared.views import region as region_view
# shared district view
from core.apps.shared.views import district as dis_view
# shared place view
from core.apps.shared.views import place as pl_view


urlpatterns = [
    # region
    path('region/', include(
        [
            path('list/', region_view.RegionListApiView.as_view(), name='region-list-api'),
        ],
    )),
    # district
    path('disctrict/', include(
        [
            path('list/', dis_view.DistrictListApiView.as_view(), name='district-list-api'),
            path('create/', dis_view.DistrictCreateApiView.as_view(), name='district-create-api'),
        ],
    )),
    # place
    path('place/', include(
        [
            path('list/', pl_view.PlaceListApiView.as_view(), name='place-list-api'),
            path('create/', pl_view.PlaceCreateApiView.as_view(), name='place-create-api'),
        ]
    )),
]   