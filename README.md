# Invoice & Receipt Intelligence API 

A production-ready OCR and document intelligence API for extracting structured data from invoices and receipts.

Built with **FastAPI**, **Tesseract OCR**, and a modular parsing pipeline.  
Designed for **easy deployment**, **RapidAPI distribution**, and **real-world usage**.

---

##  Features

- OCR for images and PDFs
- Invoice & receipt text extraction
- Structured field parsing:
  --- Vendor
  --- Invoice number
  --- Invoice date
  --- Total amount
- Confidence scoring per extracted field
- Developer-friendly JSON responses
- Swagger (OpenAPI) documentation
- Ready for Render (free) deployment
- RapidAPI compatible

---

##  Project Structure


---

##  Requirements

### System Dependencies
- Python 3.10+
- Tesseract OCR
- Poppler (for PDF support)

#### Windows
Install Tesseract from:
https://github.com/UB-Mannheim/tesseract/wiki

Ensure `tesseract` is available in PATH:
```bat
tesseract --version



