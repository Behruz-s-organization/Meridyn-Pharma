from django.urls import path, include

# shared region view
from core.apps.shared.views import region as region_view
# shared district view
from core.apps.shared.views import district as dis_view
# shared place view
from core.apps.shared.views import place as pl_view
# shared doctor view
from core.apps.shared.views import doctor as dc_view
# shared pharmacy view
from core.apps.shared.views import pharmacy as ph_view

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
            path('<int:id>/', dis_view.DistrictDeleteUpdateApiView.as_view(), name='district-update-delete-api'),
        ],
    )),
    # place
    path('place/', include(
        [
            path('list/', pl_view.PlaceListApiView.as_view(), name='place-list-api'),
            path('create/', pl_view.PlaceCreateApiView.as_view(), name='place-create-api'),
            path('<int:id>/', pl_view.PlaceDeleteUpdateApiView.as_view(), name='place-update-delete-api'),
        ]
    )),
    # doctor
    path('doctor/', include(
        [
            path('list/', dc_view.DoctorListApiView.as_view(), name='doctor-list-api'),
            path('create/', dc_view.DoctorCreateApiView.as_view(), name='doctor-create-api'),
            path('<int:id>/', dc_view.DoctorDeleteUpdateApiView.as_view(), name='doctor-update-delete-api'),
        ]
    )),
    path('pharmacy/', include(
        [
            path('list/', ph_view.PharmacyListApiView.as_view(), name='pharmacy-list-api'),
            path('create/', ph_view.PharmacyCreateApiView.as_view(), name='pharmacy-create-api'),
        ]
    )),
]   