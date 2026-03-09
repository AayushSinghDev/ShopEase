import io
from django.http import HttpResponse


def generate_invoice_pdf(order):
    """
    ReportLab se professional PDF invoice generate karo.
    reportlab install hona chahiye: pip install reportlab
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate, Table, TableStyle,
            Paragraph, Spacer, HRFlowable
        )
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
    except ImportError:
        # ReportLab install nahi hai — plain text fallback
        return _text_invoice_fallback(order)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=15 * mm, bottomMargin=15 * mm,
        leftMargin=20 * mm, rightMargin=20 * mm
    )

    elements = []
    styles = getSampleStyleSheet()

    NAVY = colors.HexColor('#0d1b3e')
    ORANGE = colors.HexColor('#f5a623')
    LIGHT_GRAY = colors.HexColor('#f8f9fa')
    MID_GRAY = colors.HexColor('#888888')

    # ── 1. Header ──────────────────────────────────────────────────────────────
    header_style = ParagraphStyle(
        'Header', fontSize=22, fontName='Helvetica-Bold',
        textColor=ORANGE, alignment=TA_LEFT,
    )
    sub_style = ParagraphStyle(
        'Sub', fontSize=9, fontName='Helvetica',
        textColor=colors.white, alignment=TA_LEFT,
    )
    invoice_style = ParagraphStyle(
        'Invoice', fontSize=14, fontName='Helvetica-Bold',
        textColor=colors.white, alignment=TA_RIGHT,
    )

    header_data = [[
        Paragraph('🛍 ShopEase', header_style),
        Paragraph(f'INVOICE<br/><font size=9>#{order.pk}</font>', invoice_style),
    ]]
    header_table = Table(header_data, colWidths=['60%', '40%'])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('LEFTPADDING', (0, 0), (0, 0), 16),
        ('RIGHTPADDING', (-1, -1), (-1, -1), 16),
        ('ROUNDEDCORNERS', [8]),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 12))

    # ── 2. Info Row (Invoice details + Billing address) ──────────────────────
    info_style = ParagraphStyle('Info', fontSize=9, fontName='Helvetica', leading=14)
    label_style = ParagraphStyle('Label', fontSize=8, fontName='Helvetica-Bold',
                                 textColor=MID_GRAY)

    addr = order.address
    left_text = (
        f'<b>Invoice #:</b> {order.pk}<br/>'
        f'<b>Date:</b> {order.created_at.strftime("%d %b %Y")}<br/>'
        f'<b>Payment:</b> {order.get_payment_method_display()}<br/>'
        f'<b>Status:</b> {order.status.title()}'
    )
    right_text = (
        f'<b>Bill To:</b><br/>'
        f'{addr.full_name}<br/>'
        f'{addr.house}<br/>'
        f'{addr.city}, {addr.state} - {addr.pincode}<br/>'
        f'Ph: {addr.phone}'
    )
    info_data = [[
        Paragraph(left_text, info_style),
        Paragraph(right_text, info_style),
    ]]
    info_table = Table(info_data, colWidths=['50%', '50%'])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('ROUNDEDCORNERS', [6]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 16))

    # ── 3. Items Table ─────────────────────────────────────────────────────────
    th_style = ParagraphStyle('TH', fontSize=9, fontName='Helvetica-Bold',
                              textColor=colors.white)
    td_style = ParagraphStyle('TD', fontSize=9, fontName='Helvetica')

    items = order.items.select_related('product')
    table_data = [
        [
            Paragraph('#', th_style),
            Paragraph('Item', th_style),
            Paragraph('Qty', th_style),
            Paragraph('Unit Price', th_style),
            Paragraph('Total', th_style),
        ]
    ]
    for idx, item in enumerate(items, start=1):
        unit = round(float(item.subtotal) / item.quantity, 2) if item.quantity else item.product_price
        row_bg = LIGHT_GRAY if idx % 2 == 0 else colors.white
        table_data.append([
            Paragraph(str(idx), td_style),
            Paragraph(item.product_name, td_style),
            Paragraph(str(item.quantity), td_style),
            Paragraph(f'Rs.{unit}', td_style),
            Paragraph(f'Rs.{item.subtotal}', td_style),
        ])

    items_table = Table(table_data, colWidths=[20, 200, 40, 80, 80])
    style_list = [
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e7ff')),
        ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
        ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
        ('ROUNDEDCORNERS', [4]),
    ]
    for i in range(1, len(table_data)):
        if i % 2 == 0:
            style_list.append(('BACKGROUND', (0, i), (-1, i), LIGHT_GRAY))
    items_table.setStyle(TableStyle(style_list))
    elements.append(items_table)
    elements.append(Spacer(1, 14))

    # ── 4. Totals Section ──────────────────────────────────────────────────────
    right_style = ParagraphStyle('Right', fontSize=9, fontName='Helvetica', alignment=TA_RIGHT)
    right_bold = ParagraphStyle('RightBold', fontSize=11, fontName='Helvetica-Bold',
                                alignment=TA_RIGHT, textColor=NAVY)
    total_orange = ParagraphStyle('TotalOrange', fontSize=13, fontName='Helvetica-Bold',
                                  alignment=TA_RIGHT, textColor=ORANGE)

    totals_rows = [
        ['', Paragraph('Subtotal', right_style), Paragraph(f'Rs.{order.subtotal}', right_style)],
    ]
    if order.discount_amount:
        totals_rows.append([
            '', Paragraph('Discount', right_style),
            Paragraph(f'- Rs.{order.discount_amount}', right_style)
        ])
    shipping_text = 'FREE' if float(order.shipping) == 0 else f'Rs.{order.shipping}'
    totals_rows.append(['', Paragraph('Shipping', right_style), Paragraph(shipping_text, right_style)])
    totals_rows.append(['', Paragraph('Tax (5%)', right_style), Paragraph(f'Rs.{order.tax}', right_style)])
    totals_rows.append(['', Paragraph('GRAND TOTAL', right_bold), Paragraph(f'Rs.{order.total}', total_orange)])

    totals_table = Table(totals_rows, colWidths=[260, 120, 80])
    totals_table.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LINEABOVE', (1, -1), (-1, -1), 1.5, NAVY),
        ('TOPPADDING', (0, -1), (-1, -1), 8),
    ]))
    elements.append(totals_table)
    elements.append(Spacer(1, 20))

    # ── 5. Footer ──────────────────────────────────────────────────────────────
    elements.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#e0e7ff')))
    elements.append(Spacer(1, 8))

    footer_center = ParagraphStyle('FooterC', fontSize=9, fontName='Helvetica',
                                   textColor=MID_GRAY, alignment=TA_CENTER)
    elements.append(Paragraph('Thank you for shopping with ShopEase!', footer_center))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(
        'This is a computer generated invoice. No signature required. | support@shopease.com',
        footer_center
    ))

    doc.build(elements)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ShopEase_Invoice_{order.pk}.pdf"'
    return response


def _text_invoice_fallback(order):
    """ReportLab nahi hai toh plain text invoice return karo."""
    lines = [
        f"SHOPEASE INVOICE",
        f"================",
        f"Invoice #: {order.pk}",
        f"Date: {order.created_at.strftime('%d %b %Y')}",
        f"Payment: {order.get_payment_method_display()}",
        f"Status: {order.status.title()}",
        f"",
        f"Bill To: {order.address.full_name}",
        f"Address: {order.address.house}, {order.address.city}",
        f"         {order.address.state} - {order.address.pincode}",
        f"Phone: {order.address.phone}",
        f"",
        f"{'ITEM':<30} {'QTY':>5} {'PRICE':>10}",
        f"{'-'*47}",
    ]
    for item in order.items.all():
        lines.append(f"{item.product_name[:28]:<30} {item.quantity:>5} Rs.{item.subtotal:>8}")
    lines += [
        f"{'-'*47}",
        f"{'Subtotal':>36} Rs.{order.subtotal}",
        f"{'Tax':>36} Rs.{order.tax}",
        f"{'Shipping':>36} Rs.{order.shipping}",
        f"{'TOTAL':>36} Rs.{order.total}",
        f"",
        f"Thank you for shopping with ShopEase!",
    ]
    content = '\n'.join(lines)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="ShopEase_Invoice_{order.pk}.txt"'
    return response
