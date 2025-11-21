from django.urls import path, include

# shared region view
from core.apps.shared.views import region as region_view


urlpatterns = [
    path('region/', include(
        [
            path('list/', region_view.RegionListApiView.as_view(), name='region-list-api'),
        ],
    )),
]