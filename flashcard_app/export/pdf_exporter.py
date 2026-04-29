from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import database as db
import os

def export_to_pdf(deck_id, deck_name, filename):
    cards = db.get_cards(deck_id)
    if not cards:
        return False
    
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    title_style.alignment = 1 # Center
    
    elements.append(Paragraph(f"Deck: {deck_name}", title_style))
    elements.append(Spacer(1, 20))
    
    card_style = ParagraphStyle(
        'CardStyle',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
        alignment=1, # Center
    )
    
    data = []
    # Header row
    data.append([Paragraph("<b>FRONT</b>", card_style), Paragraph("<b>BACK</b>", card_style)])
    
    for _, front, back in cards:
        # One row per card: Front on left, Back on right
        data.append([
            Paragraph(front, card_style),
            Paragraph(back, card_style)
        ])
        
    # Create table: 2 columns of equal width (approx 260 points each)
    table = Table(data, colWidths=[260, 260], repeatRows=1)
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey), # Header background
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
    ]))
    
    elements.append(table)
    try:
        doc.build(elements)
        return True
    except Exception as e:
        print(f"PDF Export Error: {e}")
        return False
