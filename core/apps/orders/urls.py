from django.urls import path, include

# orders product views
from core.apps.orders.views import product as product_view
# orders order views
from core.apps.orders.views import order as order_view
# orders distributed product
from core.apps.orders.views import distributed_product as dp_view


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
            path('<int:id>/send_pdf/', order_view.SendFileToTelegramApiView.as_view(), name='order-send-pdf-api'),
        ]
    )),


    path('distributed_product/', include(
        [
            path('create/', dp_view.DistributedProductCreateApiView.as_view(), name='distributed-product-create-api'),
        ]
    )),
]
