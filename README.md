RESCUER: The Virtue Intelligence Layer 🏥

Hack-Nation Global AI Hackathon Submission
Track: Databricks / Virtue Foundation (Challenge #1)
Team: Engineers (Maths & Data Logic Focus)

📖 The Problem

The Virtue Foundation sits on a goldmine of data: thousands of medical facility assessment reports. However, this data is unstructured (PDFs, text notes), making it impossible to query. Matching a patient to the nearest hospital with a functioning MRI scanner currently takes days of manual reading.

💡 The Solution

Rescuer is an Intelligent Document Parsing (IDP) agent that transforms unstructured medical reports into a strictly typed, geolocated "Ground Truth".

Unlike standard chatbots, Rescuer uses a deterministic engineering approach:

Strict Schema Enforcement: Uses Pydantic to force the AI to output valid JSON only.

Resource Quantization: Classifies equipment as functional, broken, or missing.

Critical Alerting: Automatically flags life-threatening shortages (e.g., "No Oxygen").

Decoupled Architecture: Python Backend (Logic) + Lovable Frontend (Visualization) connected via secure tunnels.

🛠️ Tech Stack

Core Logic: Python 3.10

API Framework: FastAPI

AI Engine: OpenAI GPT-4o (Structured Outputs)

Data Validation: Pydantic (Strict Types)

Ingestion: pdfplumber & PyMuPDF (Advanced Layout Analysis)

Tunneling: Ngrok / VS Code DevTunnels

Frontend: React (generated via Lovable.dev)

🚀 Installation & Setup

1. Clone the Repository

git clone [https://github.com/matthieugomez31/hackathon-bridging-medical-desert.git](https://github.com/matthieugomez31/hackathon-bridging-medical-desert.git)
cd hackathon-bridging-medical-desert


2. Set up Virtual Environment

# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate


3. Install Dependencies

pip install -r requirements.txt


4. Configure Environment

Create a .env file in the root directory:

OPENAI_API_KEY=sk-proj-YOUR_OPENAI_KEY_HERE


▶️ Usage

Running the Backend (The Brain)

To start the FastAPI server with hot-reload:

python -m uvicorn src.api:app --reload


The API will be available at http://127.0.0.1:8000

Exposing to Frontend (The Tunnel)

Since the Frontend is hosted on Lovable (Cloud), you must open a tunnel:

# Option 1: Using Ngrok (Recommended)
ngrok http 8000

# Option 2: Python Native Tunnel (Included in repo)
python start_tunnel.py


Copy the forwarding URL (e.g., https://xxxx.ngrok-free.app) and configure it in the Lovable Frontend.

📂 Project Structure

virtue-hackathon/
├── data/
│   ├── raw/             # Drag & Drop PDFs here for testing
│   └── temp/            # Temporary processing folder
├── src/
│   ├── __init__.py
│   ├── agent.py         # AI Logic (GPT-4o + Prompts)
│   ├── api.py           # FastAPI Endpoints
│   ├── ingest.py        # Advanced PDF Text Extraction
│   └── models.py        # Pydantic Data Schemas (The "Source of Truth")
├── start_tunnel.py      # Auto-tunneling script
├── requirements.txt     # Python dependencies
└── README.md            # You are here


🧠 Key Engineering Decisions

Why Pydantic? In healthcare, "hallucination" is dangerous. We use Pydantic to strictly validate every output from the LLM. If the AI cannot fit the data into our schema, we prefer a null value over a guess.

Simulation Mode: To ensure stability during the hackathon demo, the agent includes a fallback "Mock Mode" that serves realistic dummy data if API quotas are hit or connectivity fails.

Clean Ingestion: We implemented a custom cleaning pipeline in ingest.py to strip headers, footers, and OCR noise before feeding text to the context window, optimizing token usage and accuracy.

👥 Team

Engineering Students Team - Bringing mathematical rigour to AI.

Backend & Architecture: Matthieu Gomez, Sohel Dinoo

Frontend & UX: François Cacheux

Data Engineering: Marcu-Andria Castelli
