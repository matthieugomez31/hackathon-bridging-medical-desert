import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

def create_test_pdf(filename="data/raw/test_medical_report.pdf"):
    """
    Generates a realistic fake medical assessment report for the Virtue Foundation challenge.
    Includes: Header, unstructured narrative, equipment status, and critical alerts.
    """
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # --- Header ---
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2*cm, height - 2*cm, "VIRTUE FOUNDATION - FACILITY ASSESSMENT REPORT")
    
    c.setFont("Helvetica", 10)
    c.drawString(2*cm, height - 2.8*cm, "Date: February 7, 2026")
    c.drawString(2*cm, height - 3.2*cm, "Assessor: Dr. Sarah Osei")
    c.line(2*cm, height - 3.5*cm, width - 2*cm, height - 3.5*cm)
    
    # --- Facility Info (Unstructured) ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2*cm, height - 5*cm, "1. FACILITY DETAILS")
    
    c.setFont("Helvetica", 11)
    text_object = c.beginText(2*cm, height - 5.8*cm)
    text_object.setFont("Helvetica", 11)
    text_object.textLines("""
    Facility Name: Hope Valley District Hospital
    Location: Northern Region, Tamale District, 15km east of Highway N2.
    Type: District Hospital serving approx. 20,000 residents.
    GPS Coordinates (Est.): 9.4075 N, 0.8534 W
    """)
    c.drawText(text_object)
    
    # --- Narrative (The Trap for AI) ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2*cm, height - 9*cm, "2. SITE OBSERVATIONS")
    
    text_object = c.beginText(2*cm, height - 9.8*cm)
    text_object.setFont("Helvetica", 11)
    text_object.setLeading(14)
    text_object.textLines("""
    Upon arrival, the facility appeared clean but overcrowded. We met with the 
    Medical Superintendent. The power supply is unstable, relying on a backup 
    generator that fails frequently.
    
    Staffing is currently adequate for general care but lacks specialists. 
    There are 3 General Practitioners and 8 Nurses on duty. 
    However, the surgeon is only available on Tuesdays.
    Specialties available: Pediatrics, Maternity, General Medicine.
    """)
    c.drawText(text_object)
    
    # --- Equipment Status (Structured-ish) ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2*cm, height - 14*cm, "3. CRITICAL EQUIPMENT INVENTORY")
    
    y = height - 15*cm
    c.setFont("Helvetica", 11)
    
    equipment_list = [
        "- X-Ray Machine: BROKEN (Tube failure, awaiting parts since Jan 2025)",
        "- Ultrasound Scanner: FUNCTIONAL (1 unit, GE Logiq)",
        "- MRI Scanner: NONE",
        "- Incubators: FUNCTIONAL (2 units in Neonatal Ward)",
        "- Oxygen Concentrators: FUNCTIONAL (3 units)"
    ]
    
    for item in equipment_list:
        c.drawString(2.5*cm, y, item)
        y -= 0.8*cm
        
    # --- Alerts ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2*cm, y - 1*cm, "4. CRITICAL SHORTAGES & RISKS")
    
    c.setFont("Helvetica-Oblique", 11)
    c.setFillColorRGB(0.8, 0, 0) # Red color
    c.drawString(2*cm, y - 2*cm, "URGENT: Severe shortage of Anti-Malaria drugs (Artemether).")
    c.drawString(2*cm, y - 2.6*cm, "URGENT: No surgical gloves remaining in stock.")
    c.setFillColorRGB(0, 0, 0) # Back to black
    
    c.save()
    print(f"✅ PDF Generated successfully: {filename}")

if __name__ == "__main__":
    create_test_pdf()
