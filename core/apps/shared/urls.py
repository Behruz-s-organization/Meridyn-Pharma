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
# shared plan view
from core.apps.shared.views import plan as plan_view
# shared location view
from core.apps.shared.views import location as location_view
# shared tour plan view
from core.apps.shared.views import tour_plan as tp_view
# shared factory view
from core.apps.shared.views import factory as factory_view
# shared support view
from core.apps.shared.views import support as support_view
# shared dis product
from core.apps.shared.views import dis_product as dp_view


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
    path('plan/', include(
        [
            path('', plan_view.PlanApiView.as_view(), name='plan-create-list-api'),
            path('<int:id>/complite/', plan_view.ComplitePlanApiView.as_view(), name='complite-plan-api'),
            path('<int:id>/delete/', plan_view.PlanDeleteApiView.as_view(), name='plan-delete-api'),
            path('<int:id>/update/', plan_view.PlanUpdateApiView.as_view(), name='plan-update-api'),
        ]
   )),
    path('location/', include(
        [
            path('list/', location_view.LocationListApiView.as_view(), name='location-list-api'),
            path('create/', location_view.LocationCreateApiView.as_view(), name='create-location-api'),
            path('send/', location_view.UserLocationApiView.as_view(), name='send-user-location-api'),
        ]
    )),
    path('tour_plan/', include(
        [
            path('list/', tp_view.TourPlanListApiView.as_view(), name='tour-plan-list-api'),
            path('<int:id>/update/', tp_view.TourPlanUpdateApiView.as_view()),
            path('create/', tp_view.TourPlanCreateApiView.as_view(), name='tour-plan-create-api'),
        ]
    )),
    path('factory/', include(
        [
            path('list/', factory_view.FactoryListApiView.as_view(), name='factory-list-api'),
        ],
    )),
    path('support/', include(
        [
            path('send/', support_view.SupportCreateApiView.as_view(), name='support-create-api'),
            path('list/', support_view.SupportListApiView.as_view(), name='support-list-api'),
        ]
    )),
    path('distributed_product/', include(
        [
            path('list/', dp_view.DistributedProductListApiView.as_view()),
        ]
    )),
]