from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from backend.prodoc_service import run_prodoc_on_text
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path



app = FastAPI(title="PRODOC API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



BASE_DIR = Path(__file__).resolve().parent

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    html_path = BASE_DIR / "templates" / "index.html"
    return html_path.read_text(encoding="utf-8")


import pdfplumber
from io import BytesIO


def extract_text_from_pdf(file_bytes: bytes) -> str:
    text_chunks = []

    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)

    return "\n\n".join(text_chunks)

@app.post("/upload")
async def upload_contract(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF files are supported"}

    file_bytes = await file.read()
    extracted_text = extract_text_from_pdf(file_bytes)

    if not extracted_text.strip():
        return {"error": "No text could be extracted from the PDF"}

    result = run_prodoc_on_text(
        contract_text=extracted_text,
        contract_title=file.filename
    )

    return result
