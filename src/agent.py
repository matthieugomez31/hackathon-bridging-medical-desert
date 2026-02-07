import os
from openai import OpenAI
from dotenv import load_dotenv
from src.models import HospitalFacility

# Load environment variables
load_dotenv()

def get_openai_client():
    """Helper to initialize the client with error handling."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("❌ OPENAI_API_KEY not found in .env file.")
    return OpenAI(api_key=api_key)

def analyze_document(text_content: str) -> HospitalFacility | None:
    """
    Sends raw text to GPT-4o and forces a structured JSON response 
    adhering to the HospitalFacility Pydantic model.
    """
    client = get_openai_client()

    # System prompt is the 'Role' we give the AI
    system_prompt = """
    You are an expert Data Analyst for the Virtue Foundation (NGO).
    Your task is to extract structured medical capacity data from field reports.
    
    CRITICAL RULES:
    1. Be strictly factual. Do not hallucinate equipment not mentioned.
    2. If coordinates (lat/lon) are missing, leave them null.
    3. Identify critical shortages (e.g., 'broken X-ray', 'lack of antibiotics').
    4. Categorize the facility type conservatively.
    """

    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",  # Best model for structured output
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this medical report and extract data:\n\n{text_content}"},
            ],
            response_format=HospitalFacility,
        )
        
        # Return the validated Pydantic object
        return completion.choices[0].message.parsed

    except Exception as e:
        print(f"❌ OpenAI API Error: {e}")
        return None