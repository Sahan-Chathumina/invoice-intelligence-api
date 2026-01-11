import re

class InvoiceParser:
    @staticmethod
    def extract_fields(text: str) -> dict:
        data = {}

        vendor_match = re.search(r"(Invoice From|Vendor|Seller)[:\s]+(.+)", text, re.IGNORECASE)
        total_match = re.search(r"(Total Amount|Grand Total|Total)[:\s]+([\d,]+\.\d{2})", text)
        date_match = re.search(r"(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})", text)
        invoice_no_match = re.search(r"(Invoice No|Invoice #|Invoice Number)[:\s]+(\S+)", text)

        data["vendor"] = vendor_match.group(2) if vendor_match else None
        data["total"] = float(total_match.group(2).replace(",", "")) if total_match else None
        data["invoice_date"] = date_match.group(1) if date_match else None
        data["invoice_number"] = invoice_no_match.group(2) if invoice_no_match else None

        return data
