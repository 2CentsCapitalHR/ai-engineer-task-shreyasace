from typing import Dict
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from textwrap import wrap


def build_summary_pdf(report: Dict) -> bytes:
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    y = height - 40

    def line(txt, dy=16, bold=False):
        nonlocal y
        if bold:
            c.setFont("Helvetica-Bold", 11)
        else:
            c.setFont("Helvetica", 10)
        lines = wrap(txt, 100)
        for l in lines:
            c.drawString(40, y, l)
            y -= dy

    line("ADGM Corporate Agent — Executive Summary", bold=True)
    line("")
    line(f"Process: {report.get('process')}")
    line(f"Documents uploaded: {report.get('documents_uploaded')}  Required: {report.get('required_documents')}")

    missing = report.get('missing_documents') or []
    if missing:
        line("Missing:", bold=True)
        for m in missing:
            line(f"- {m}")

    issues = report.get('issues_found') or []
    if issues:
        line("")
        line("Top Issues:", bold=True)
        for i, iss in enumerate(issues[:10], 1):
            line(f"{i}. {iss.get('document')}: {iss.get('issue')} [{iss.get('severity')}]")

    c.showPage()
    c.save()
    return buf.getvalue()
