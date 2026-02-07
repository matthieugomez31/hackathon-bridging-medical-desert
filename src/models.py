from pydantic import BaseModel, Field
from typing import List, Optional, Literal

# --- Enums for strict categorization ---
HospitalType = Literal["clinic", "hospital", "specialized_center", "mobile_unit", "unknown"]
EquipmentStatus = Literal["functional", "broken", "maintenance_needed", "unknown"]

class MedicalEquipment(BaseModel):
    """Represents a single piece of medical equipment and its status."""
    name: str = Field(..., description="Name of the equipment (e.g., 'MRI Scanner', 'X-Ray Machine', 'Incubator')")
    status: EquipmentStatus = Field(..., description="Current operational status of the equipment")
    count: int = Field(default=1, description="Number of units available")

class Staffing(BaseModel):
    """Details about the medical staff available at the facility."""
    doctors_count: int = Field(default=0, description="Number of doctors present")
    nurses_count: int = Field(default=0, description="Number of nurses present")
    specialties: List[str] = Field(default_factory=list, description="List of medical specialties available (e.g., 'Pediatrics', 'Cardiology')")

class HospitalFacility(BaseModel):
    """
    Main model representing a medical facility extracted from a report.
    This acts as the Ground Truth for the medical desert analysis.
    """
    name: str = Field(..., description="Official name of the medical facility")
    location_raw: str = Field(..., description="Raw location string as found in the text")
    
    # Coordinates are crucial for the 'Medical Desert' map visualization
    latitude: Optional[float] = Field(None, description="Estimated latitude if mentioned or inferable")
    longitude: Optional[float] = Field(None, description="Estimated longitude if mentioned or inferable")
    
    facility_type: HospitalType = Field(..., description="Classification of the facility")
    
    # Detailed resources
    equipment: List[MedicalEquipment] = Field(default_factory=list, description="List of medical equipment found in the report")
    staffing: Optional[Staffing] = Field(None, description="Staffing details")
    
    # Critical analysis for the NGO
    critical_shortages: List[str] = Field(default_factory=list, description="List of critical items or staff explicitly missing (e.g., 'No oxygen', 'No antibiotics')")
    operational_capacity_score: int = Field(..., description="A score from 0 to 100 estimating the overall operational readiness based on text")