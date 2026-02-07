import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from src.models import HospitalFacility

load_dotenv()

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️ No API key found in environment variables.")
        return None
    return OpenAI(api_key=api_key)

def get_mock_data():
    """
    Fallback data for when the API is down or quota is exceeded.
    Allows the Frontend to continue working without crashing.
    """
    print("⚠️ SWITCHING TO SIMULATION MODE (MOCK DATA) ⚠️")
    return HospitalFacility(
        name="[SIMULATION] Hope Valley District Hospital",
        location_raw="Northern Region, Tamale District",
        latitude=9.4075,
        longitude=-0.8534,
        facility_type="hospital",
        equipment=[
            {"name": "X-Ray Machine", "status": "broken", "count": 1},
            {"name": "Ultrasound Scanner", "status": "functional", "count": 1},
            {"name": "Incubators", "status": "functional", "count": 2}
        ],
        staffing={
            "doctors_count": 3,
            "nurses_count": 8,
            "specialties": ["Pediatrics", "Maternity", "General Medicine"]
        },
        critical_shortages=["Anti-Malaria drugs", "Surgical gloves"],
        operational_capacity_score=45
    )

def analyze_document(text_content: str) -> HospitalFacility | None:
    client = get_openai_client()

    # If no client is available (or known quota error), return Mock data directly
    if not client:
        return get_mock_data()

    system_prompt = """
    You are an expert Data Analyst for the Virtue Foundation.
    Extract medical capacity data strictly following the JSON schema.
    """

    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": system_prompt},
                # Truncate text if too long to avoid token limits
                {"role": "user", "content": f"Analyze this report:\n\n{text_content[:15000]}"}, 
            ],
            response_format=HospitalFacility,
        )
        return completion.choices[0].message.parsed

    except Exception as e:
        print(f"❌ OpenAI Error ({str(e)})")
        # FALLBACK LOGIC: Instead of crashing, return the simulation data
        return get_mock_data()