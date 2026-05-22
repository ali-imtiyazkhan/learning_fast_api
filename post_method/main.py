from fastapi import FastAPI, HTTPException
from typing import List, Optional, Annotated
from pydantic import BaseModel, Field

import json
import os

app = FastAPI()

def load_data():
    if not os.path.exists('patients.json'):
        return []
    with open('patients.json', 'r') as file:
        return json.load(file)

patients = load_data()

# create a model for the patient
class Patient(BaseModel):
    id:      Annotated[int, Field(gt=0,description="Enter the id")]
    name:    Annotated[str, Field(min_length=2, description="Enter the name")]
    age:     Annotated[int, Field(ge=0, le=120, description="Enter the age")]
    address: Annotated[str, Field(min_length=5, description="Enter the address")]
    phone:   Annotated[str, Field(description="Enter the phone number")]
    disease: Annotated[str, Field(description ="Enter the name of the disease")]


# get all the patients detail
@app.get("/patients")
def get_all_patients():
    return patients

# get the specific patients detail
@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    for p in patients:
        if p["id"] == patient_id:
            return p
    raise HTTPException(status_code=404, detail="Patient not found")

# make a new patients entry
@app.post("/patients")
def create_patient(patient: Patient):
    patients.append(patient.model_dump())
    return patient

# delete the specific patient
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    for i, p in enumerate(patients):
        if p["id"] == patient_id:
            patients.pop(i)
            return {"message": "Patient deleted"}
    raise HTTPException(status_code=404, detail="Patient not found")