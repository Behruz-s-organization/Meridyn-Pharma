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
from core.apps.dashboard.views.doctor import DoctorViewSet, DoctorExportView
# region
from core.apps.dashboard.views import region as region_views
# plan 
from core.apps.dashboard.views.plan import PlanViewSet
# place
from core.apps.dashboard.views.place import PlaceViewSet
# pharmacy
from core.apps.dashboard.views.pharmacy import PharmacyViewSet, PharmacyExportView
# product
from core.apps.dashboard.views.product import ProductViewSet
# factory
from core.apps.dashboard.views.factory import FactoryViewSet
# tour plan
from core.apps.dashboard.views.tour_plan import TourPlanViewSet
# order
from core.apps.dashboard.views.order import OrderViewSet
# payment
from core.apps.dashboard.views.payment import PaymentListApiView
# location
from core.apps.dashboard.views.location import LocationViewSet, UserLocationViewSet
# support
from core.apps.dashboard.views.support import SupportListApiView
# distibuted products
from core.apps.dashboard.views.dis_prod import DistributedProductListApiView
# send message
from core.apps.dashboard.views.send_message import SendMessageToEmployee


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
    path('payment/', include(
        [
            path('list/', PaymentListApiView.as_view(), name='payment-list-api'),
        ]
    )),
    # -------------- support --------------
    path('support/', include(
        [
            path('list/', SupportListApiView.as_view(), name='support-list-api'),
        ]
    )),
    # -------------- distributed products --------------
    path('distributed_product/', include(
        [
            path('list/', DistributedProductListApiView.as_view(), name='distributed-product-list-api'),
        ]
    )),

    # -------------- send message --------------
    path('send_message/', SendMessageToEmployee.as_view()),

    # -------------- pharmacy --------------
    path('pharmacy/export/', PharmacyExportView.as_view()),

    # -------------- doctor --------------
    path('doctor/export/', DoctorExportView.as_view()),
]


### ViewSets ###
router = DefaultRouter()
router.register("doctor", DoctorViewSet)
router.register("plan", PlanViewSet)
router.register("place", PlaceViewSet)
router.register("pharmacy", PharmacyViewSet)
router.register("product", ProductViewSet)
router.register("factory", FactoryViewSet)
router.register("tour_plan", TourPlanViewSet)
router.register("order", OrderViewSet)
router.register("location", LocationViewSet)
router.register("user_location", UserLocationViewSet)


urlpatterns += router.urls