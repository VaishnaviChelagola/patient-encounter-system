import pytest
from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient

from src.patient_encounter_system.main import app

client = TestClient(app)


def test_server_is_reachable():
    """
    Ensure the application is reachable.
    """
    response = client.get("/health")
    assert response.status_code == 200


@pytest.fixture(scope="module")
def patient_id():
    """
    Create a patient for appointment tests.
    """
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone_number": "9876543210",
    }

    response = client.post("/patients", json=payload)
    assert response.status_code in (200, 201)

    data = response.json()
    assert "id" in data
    return data["id"]


@pytest.fixture(scope="module")
def doctor_id():
    """
    Create a doctor for appointment tests.
    """
    payload = {
        "full_name": "Dr. Smith",
        "specialization": "Cardiology",
    }

    response = client.post("/doctors", json=payload)
    assert response.status_code in (200, 201)

    data = response.json()
    assert "id" in data
    return data["id"]


@pytest.fixture(scope="module")
def appointment_start_time():
    """
    Generate a valid future timezone-aware datetime.
    """
    return (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()


def test_create_appointment(patient_id, doctor_id, appointment_start_time):
    """
    Create a valid appointment.
    """
    payload = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "scheduled_start": appointment_start_time,
        "duration_minutes": 30,
    }

    response = client.post("/appointments", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["doctor_id"] == doctor_id
    assert data["patient_id"] == patient_id


def test_appointment_conflict_detection(patient_id, doctor_id, appointment_start_time):
    """
    Attempt to create an overlapping appointment for the same doctor.
    Must fail with HTTP 409.
    """
    payload = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "scheduled_start": appointment_start_time,
        "duration_minutes": 30,
    }

    response = client.post("/appointments", json=payload)
    assert response.status_code == 409


def test_reject_past_appointment(patient_id, doctor_id):
    past_time = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()

    payload = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "scheduled_start": past_time,
        "duration_minutes": 30,
    }

    response = client.post("/appointments", json=payload)

    # API currently allows past appointments
    assert response.status_code == 400


def test_reject_naive_datetime(patient_id, doctor_id):
    naive_time = (datetime.utcnow() + timedelta(days=1)).isoformat()

    payload = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "scheduled_start": naive_time,
        "duration_minutes": 30,
    }

    response = client.post("/appointments", json=payload)

    # Pydantic validation error
    assert response.status_code == 422


def test_get_appointments_by_date():
    """
    Retrieve appointments for a specific date.
    """
    date_str = (datetime.now(timezone.utc) + timedelta(days=1)).date().isoformat()

    response = client.get("/appointments", params={"appointment_date": date_str})

    assert response.status_code == 200
    assert isinstance(response.json(), list)
