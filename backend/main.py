import os

from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_SECRET_KEY
)

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Medi-Trace Backend is running!"
    }


@app.get("/patients")
def get_patients():
    response = supabase.table("patients").select("*").execute()

    return {
        "patients": response.data
    }

@app.get("/patients/{patient_id}/medical-summary")
def get_medical_summary(patient_id: str):

    # Get patient information
    patient_response = (
        supabase
        .table("patients")
        .select("*")
        .eq("patient_id", patient_id)
        .execute()
    )

    # If patient doesn't exist
    if not patient_response.data:
        return {
            "error": "Patient not found"
        }

    patient = patient_response.data[0]

    # Get medical conditions
    conditions_response = (
        supabase
        .table("patient_conditions")
        .select("*")
        .eq("patient_id", patient_id)
        .execute()
    )

    # Get allergies
    allergies_response = (
        supabase
        .table("patient_allergies")
        .select("*")
        .eq("patient_id", patient_id)
        .execute()
    )

    # Get medications
    medications_response = (
        supabase
        .table("patient_medications")
        .select("*")
        .eq("patient_id", patient_id)
        .execute()
    )

    # Get medical events
    events_response = (
        supabase
        .table("medical_events")
        .select("*")
        .eq("patient_id", patient_id)
        .execute()
    )

    return {
        "patient": patient,
        "conditions": conditions_response.data,
        "allergies": allergies_response.data,
        "medications": medications_response.data,
        "medical_events": events_response.data
    }