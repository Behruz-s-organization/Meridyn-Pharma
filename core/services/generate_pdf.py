# type: ignore
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from core.apps.orders.models.order import Order
from weasyprint import HTML
from io import BytesIO
from django.conf import settings
from datetime import datetime


def generate_order_pdf(order_id):
    order = get_object_or_404(Order, id=order_id)

    html_string = render_to_string(
        "pdf/specification.html",
        {
            "order": order,
            "items": order.order_items.all(),
            "printed_at": datetime.now(),
        },
    )

    buffer = BytesIO()

    HTML(string=html_string, base_url=settings.STATIC_ROOT).write_pdf(buffer)

    buffer.seek(0)
    return buffer
