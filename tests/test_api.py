"""from datetime import datetime, timedelta
from schemas.patient import PatientCreate
from schemas.doctor import DoctorCreate
import pytest"""


def test_create_and_get_patient(client):
    payload = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
        "phone_number": "1234567890",
    }
    response = client.post("/patients", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "Alice"

    # Get the patient
    patient_id = data["id"]
    response = client.get(f"/patients/{patient_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "alice@example.com"


def test_create_and_get_doctor(client):
    payload = {"full_name": "Dr. Who", "specialization": "Time Travel"}
    response = client.post("/doctors", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "Dr. Who"
