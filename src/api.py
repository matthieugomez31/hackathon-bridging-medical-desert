from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from pathlib import Path

# --- IMPORT MARCU'S LOGIC ---
# We import the specific functions we need from ingest.py
from src.ingest import extract_text, clean_text
from src.agent import analyze_document

app = FastAPI(title="Virtue Foundation Backend", version="1.1")

# Allow Lovable/Frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "online", "ingest_engine": "Marcu's Advanced Pipeline"}

@app.post("/analyze")
async def analyze_report_endpoint(file: UploadFile = File(...)):
    """
    1. Receives PDF from Frontend.
    2. Uses Marcu's ingest logic (PyMuPDF/Plumber) to extract text.
    3. Cleans text.
    4. Sends to GPT-4o Agent.
    5. Returns JSON to Frontend.
    """
    # Create temp directory if not exists
    temp_dir = Path("data/temp")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    temp_file_path = temp_dir / file.filename

    try:
        # 1. Save file locally
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"📥 Received file: {file.filename}")

        # 2. Extract Text using Marcu's robust function
        # extract_text expects a Path object and returns a dict
        extraction_result = extract_text(temp_file_path)
        raw_text = extraction_result.get("text", "")
        
        # 3. Clean the text
        cleaned_text = clean_text(raw_text)
        
        if not cleaned_text:
            raise HTTPException(status_code=400, detail="Could not extract any text from this document.")

        print(f"📄 Extracted {len(cleaned_text)} chars using {extraction_result.get('method')}")

        # 4. AI Analysis
        print("🧠 Sending to Agent...")
        result = analyze_document(cleaned_text)
        
        if not result:
            raise HTTPException(status_code=500, detail="AI Agent failed to analyze text.")

        # 5. Return JSON
        return result.model_dump()

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Optional: Clean up temp file to save space
        # if temp_file_path.exists():
        #     temp_file_path.unlink()
        pass