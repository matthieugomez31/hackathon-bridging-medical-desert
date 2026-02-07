from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from pypdf import PdfReader
from src.agent import analyze_document
# Make sure your models are defined in src/models.py as discussed before

app = FastAPI(title="Virtue Foundation Backend", version="1.0")

# --- CRITICAL: CORS Setup for Lovable ---
# This allows the Lovable website to send requests to your local machine
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (POST, GET, etc.)
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    """Simple check to see if API is running."""
    return {"status": "online", "message": "Virtue Foundation API Ready"}

@app.post("/analyze")
async def analyze_report_endpoint(file: UploadFile = File(...)):
    """
    Receives a PDF, extracts text, runs the AI agent, and returns structured JSON.
    Target format is optimized for Lovable UI (lists/tags).
    """
    temp_file_path = f"data/temp/{file.filename}"
    os.makedirs("data/temp", exist_ok=True)

    try:
        # 1. Save the uploaded file locally
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"📥 Received file: {file.filename}")

        # 2. Extract Text (Simplified logic inline for speed)
        reader = PdfReader(temp_file_path)
        text_content = ""
        for page in reader.pages:
            text_content += page.extract_text() or ""
        
        print(f"📄 Extracted {len(text_content)} characters.")

        # 3. Call the AI Agent (Your logic from src/agent.py)
        # Ensure your analyze_document function returns the Pydantic model
        result = analyze_document(text_content)
        
        if not result:
            raise HTTPException(status_code=500, detail="AI Analysis returned empty result.")

        # 4. Format Data for Lovable
        # We convert the Pydantic model to a standard dictionary (JSON)
        response_data = result.model_dump()
        
        # --- DEBUG: Print what we are sending ---
        print("✅ Sending JSON to Lovable.")
        return response_data

    except Exception as e:
        print(f"❌ Error processing file: {str(e)}")
        # Return a clean error so the frontend doesn't crash blindly
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Cleanup: remove temp file if needed, or keep for debug
        pass