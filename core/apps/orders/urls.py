from django.urls import path, include

# orders product views
from core.apps.orders.views import product as product_view
# orders order views
from core.apps.orders.views import order as order_view


urlpatterns = [
    path('product/', include(
        [
            path('list/', product_view.ProductApiView.as_view(), name='product-list-api'),
        ]
    )),
    path('order/', include(
        [
            path('list/', order_view.OrderListApiView.as_view(), name='order-list-api'),
            path('create/', order_view.OrderCreateApiView.as_view(), name='order-create-api'),
            path('<int:id>/update/', order_view.OrderUpdateApiView.as_view(), name='order-update-api'),
        ]
    )),

]
