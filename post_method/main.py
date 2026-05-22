from fastapi import FastAPI, HTTPException
from typing import Optional, Annotated
from pydantic import BaseModel, Field
import json
import os

app = FastAPI()


#  LOAD DATA 
def load_data():
    if not os.path.exists("patients.json"):
        return []

    with open("patients.json", "r") as file:
        return json.load(file)


def save_data(data):
    with open("patients.json", "w") as file:
        json.dump(data, file, indent=2)


#  MODELS 
class Patient(BaseModel):
    id: Annotated[int, Field(gt=0, description="Enter the id")]
    name: Annotated[str, Field(min_length=2, description="Enter the name")]
    age: Annotated[int, Field(ge=0, le=120, description="Enter the age")]
    address: Annotated[str, Field(min_length=5, description="Enter the address")]
    phone: Annotated[str, Field(description="Enter the phone number")]
    disease: Annotated[str, Field(description="Enter disease name")]


class UpdatePatient(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2)
    age: Optional[int] = Field(default=None, ge=0, le=120)
    address: Optional[str] = Field(default=None, min_length=5)
    phone: Optional[str] = None
    disease: Optional[str] = None


#  GET ALL PATIENTS -
@app.get("/patients")
def get_all_patients():
    return load_data()


#  GET SINGLE PATIENT 
@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    data = load_data()

    for patient in data:
        if patient["id"] == patient_id:
            return patient

    raise HTTPException(status_code=404, detail="Patient not found")


#  CREATE PATIENT 
@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()

    # check duplicate id
    for p in data:
        if p["id"] == patient.id:
            raise HTTPException(
                status_code=400,
                detail="Patient already exists"
            )

    data.append(patient.model_dump())

    save_data(data)

    return {
        "message": "Patient created successfully",
        "patient": patient
    }


#  UPDATE PATIENT 
@app.put("/edit/{patient_id}")
def update_patient(patient_id: int, patient: UpdatePatient):
    data = load_data()

    for p in data:
        if p["id"] == patient_id:

            update_data = patient.model_dump(exclude_unset=True)

            p.update(update_data)

            save_data(data)

            return {
                "message": "Patient updated successfully",
                "patient": p
            }

    raise HTTPException(status_code=404, detail="Patient not found")


#  DELETE PATIENT 
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    data = load_data()

    for i, p in enumerate(data):
        if p["id"] == patient_id:
            deleted_patient = data.pop(i)

            save_data(data)

            return {
                "message": "Patient deleted successfully",
                "patient": deleted_patient
            }

    raise HTTPException(status_code=404, detail="Patient not found")