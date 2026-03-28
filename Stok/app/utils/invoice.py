from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

def generate_invoice(company_id: int, amount: int):
    file_name = f"invoice_{company_id}_{datetime.utcnow().timestamp()}.pdf"

    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph(f"FATURA", styles["Title"]))
    content.append(Paragraph(f"Company ID: {company_id}", styles["Normal"]))
    content.append(Paragraph(f"Tutar: {amount} TL", styles["Normal"]))
    content.append(Paragraph(f"Tarih: {datetime.utcnow()}", styles["Normal"]))

    doc.build(content)

    return file_name