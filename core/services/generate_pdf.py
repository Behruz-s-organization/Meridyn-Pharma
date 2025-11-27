from datetime import datetime
from decimal import Decimal
from io import BytesIO

# django
from django.shortcuts import get_object_or_404

# reportlab
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER

from core.apps.orders.models import Order


def generate_order_pdf(order_id):
    order = get_object_or_404(Order, id=order_id)
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           rightMargin=0.5*cm, leftMargin=0.5*cm,
                           topMargin=0.5*cm, bottomMargin=0.5*cm)
    
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    title = Paragraph(f"BUYURTMA CHIPTASI", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*cm))
    
    info_data = [
        ['Buyurtma ID:', f"#{order.id}"],
        ['Sana:', order.created_at.strftime('%d.%m.%Y %H:%M') if order.created_at else 'N/A'],
        ['Fabrika:', order.factory.name if order.factory else 'Belgilanmagan'],
    ]
    
    info_table = Table(info_data, colWidths=[3*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1f4788')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.5*cm))
    
    elements.append(Paragraph("XARIDOR MA'LUMOTLARI", heading_style))
    customer_data = [
        ['Ismi:', order.user.first_name + ' ' + order.user.last_name if order.user else 'N/A'],
        ['Email:', order.user.email if order.user else 'N/A'],
        ['Telefon:', order.user.phone if hasattr(order.user, 'phone') else 'N/A'],
        ['Xodim:', order.employee_name or 'Belgilanmagan'],
    ]
    
    customer_table = Table(customer_data, colWidths=[3*cm, 12*cm])
    customer_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#333333')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(customer_table)
    elements.append(Spacer(1, 0.5*cm))
    
    elements.append(Paragraph("MAHSULOTLAR", heading_style))
    
    order_items = order.order_items.all()
    
    if order_items.exists():
        items_data = [
            ['#', 'Mahsulot', 'Miqdor', 'Narxi', 'Jami Narx'],
        ]
        
        for idx, item in enumerate(order_items, 1):
            unit_price = Decimal(str(item.total_price / item.quantity)) if item.quantity else 0
            items_data.append([
                str(idx),
                item.product.name,
                str(item.quantity),
                f"{unit_price:,.2f} so'm",
                f"{item.total_price:,.2f} so'm"
            ])
        
        items_table = Table(items_data, colWidths=[0.8*cm, 6*cm, 2*cm, 2.5*cm, 3*cm])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(items_table)
    else:
        elements.append(Paragraph("Mahsulotlar qo'shilmagan", normal_style))
    
    elements.append(Spacer(1, 0.5*cm))
    
    summary_data = [
        ['Umumiy summa:', f"{order.total_price:,.2f} so'm"],
        ['To\'langan:', f"{order.paid_price:,.2f} so'm"],
        ['Avans:', f"{order.advance:,.2f} so'm"],
        ['Qolgan to\'lov:', f"{order.overdue_price:,.2f} so'm"],
    ]
    
    summary_table = Table(summary_data, colWidths=[8*cm, 6*cm])
    summary_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('TEXTCOLOR', (0, -1), (0, -1), colors.red),
        ('TEXTCOLOR', (1, -1), (1, -1), colors.red),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
    ]))
    elements.append(summary_table)
    
    elements.append(Spacer(1, 1*cm))
    
    footer_text = f"<i>Chop etilgan sana: {datetime.now().strftime('%d.%m.%Y %H:%M')}</i>"
    footer = Paragraph(footer_text, ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    ))
    elements.append(footer)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
