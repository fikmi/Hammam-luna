from __future__ import annotations

from io import BytesIO

from django.conf import settings
from django.core.files.base import ContentFile
from django.template.loader import render_to_string

try:  # pragma: no cover - graceful fallback
    from weasyprint import HTML
except Exception:  # pragma: no cover
    HTML = None

from .models import CreditNote, Invoice


class InvoiceService:
    def _render_pdf(self, template: str, context: dict[str, object]) -> bytes:
        html = render_to_string(template, context)
        if HTML is None:
            return html.encode("utf-8")
        pdf_io = BytesIO()
        HTML(string=html, base_url=str(settings.BASE_DIR)).write_pdf(pdf_io)
        return pdf_io.getvalue()

    def generate_invoice(self, order) -> Invoice:
        pdf_bytes = self._render_pdf("billing/invoice.html", {"order": order})
        filename = f"invoice_{order.pk}.pdf"
        invoice, _ = Invoice.objects.update_or_create(
            order=order,
            defaults={"total": order.total, "currency": order.currency},
        )
        invoice.pdf.save(filename, ContentFile(pdf_bytes), save=True)
        return invoice

    def generate_credit_note(self, order) -> CreditNote:
        pdf_bytes = self._render_pdf("billing/credit_note.html", {"order": order})
        filename = f"credit_note_{order.pk}.pdf"
        credit, _ = CreditNote.objects.update_or_create(
            order=order,
            defaults={"amount": order.total},
        )
        credit.pdf.save(filename, ContentFile(pdf_bytes), save=True)
        return credit
