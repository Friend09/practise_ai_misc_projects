# api.py

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from main import process_medical_document, create_medical_analysis_chain
import os
from datetime import datetime

app = FastAPI()

# Create required directories if they don't exist
static_dir = Path("static")  # Remove the "./"
data_dir = Path("data")      # Remove the "./"
for directory in [static_dir, data_dir]:
    directory.mkdir(parents=True, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Setup templates - remove the "./"
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Generate graph visualization when loading the page
    _, graph_base64 = create_medical_analysis_chain()
    return templates.TemplateResponse(
        "index.html",
        {
            "request":request,
            "graph_base64": graph_base64
        }
    )

@app.post("/analyze-medical-document")
async def analyze_document(file: UploadFile = File(...)):
    try:
        # validate file extension
        if not file.filename.lower().endswith('.pdf'): # if file is not pdf, True
            return JSONResponse(
                status_code=400,
                content={"status":"error", "message":"Only PDF files are supported"}
            )

        # create a unique filename to avoid overwrites
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = data_dir / safe_filename

        # save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # process the document
        result = process_medical_document(str(file_path))

        return JSONResponse(content={
            "status":"success",
            "analysis":result["analysis"],
            "summary": result["summary"],
            "validation": result["validation"],
            "graph": result["graph"]
        })
    except ValueError as e:
        print(f"Error processing document: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",  # Fix typo: "erro" → "error"
                "message": "An error occurred while processing your document"
            }
        )

# optional: cleanup endpoing for maintenance
@app.delete("/cleanup")
async def cleanup_old_files():
    """clean up files older than 24 hours"""
    try:
        current_time = datetime.now()
        for file_path in data_dir.glob("*.pdf"):
            file_age = current_time - datetime.fromtimestamp(file_path.stat().st_mtime)

            if file_age.days >= 1:
                file_path.unlink()
        return JSONResponse(content={"status": "success", "message": "Cleanup completed"})
    except Exception as e:
        return JSONResponse(
                    status_code=500,
                    content={"status": "error", "message": f"Cleanup failed: {str(e)}"}
                )
