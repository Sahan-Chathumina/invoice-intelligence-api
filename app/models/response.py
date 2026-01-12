from pydantic import BaseModel, Field


class InvoiceOCRResponse(BaseModel):
    """
    Standard response model for OCR extraction endpoints.
    """

    filename: str = Field(
        ...,
        example="invoice_001.pdf",
        description="Original uploaded file name",
    )

    content_type: str = Field(
        ...,
        example="application/pdf",
        description="MIME type of the uploaded document",
    )

    raw_text: str = Field(
        ...,
        example="Invoice No: INV-001\nDate: 2024-01-01\nTotal: $250.00",
        description="Raw OCR-extracted text from the document",
    )
