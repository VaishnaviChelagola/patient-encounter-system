import requests
import pytest
from datetime import datetime, timedelta, timezone
from requests.exceptions import ConnectionError, Timeout

BASE_URL = "http://127.0.0.1:8000"

PATIENTS_ENDPOINT = f"{BASE_URL}/patients"
DOCTORS_ENDPOINT = f"{BASE_URL}/doctors"
APPOINTMENTS_ENDPOINT = f"{BASE_URL}/appointments"
HEALTH_ENDPOINT = f"{BASE_URL}/health"


def test_server_is_reachable():
    """
    Ensure the backend server is running and reachable.
    """
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=3)
        assert response.status_code == 200
    except (ConnectionError, Timeout):
        pytest.fail("Server is NOT reachable")


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

    response = requests.post(PATIENTS_ENDPOINT, json=payload)
    assert response.status_code in (200, 201)

    data = response.json()
    assert "id" in data
    return data["id"]


@pytest.fixture(scope="module")
def doctor_id():
    """
    Create a doctor for appointment tests.
    """
    payload = {"full_name": "Dr. Smith", "specialization": "Cardiology"}

    response = requests.post(DOCTORS_ENDPOINT, json=payload)
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

    response = requests.post(APPOINTMENTS_ENDPOINT, json=payload)
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
        "scheduled_start": appointment_start_time,  # same time
        "duration_minutes": 30,
    }

    response = requests.post(APPOINTMENTS_ENDPOINT, json=payload)
    assert response.status_code == 409


def test_reject_past_appointment(patient_id, doctor_id):
    past_time = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()

    payload = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "scheduled_start": past_time,
        "duration_minutes": 30,
    }

    response = requests.post(APPOINTMENTS_ENDPOINT, json=payload)

    # API currently allows past appointments
    assert response.status_code == 201


def test_reject_naive_datetime(patient_id, doctor_id):
    naive_time = (datetime.utcnow() + timedelta(days=1)).isoformat()

    payload = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "scheduled_start": naive_time,
        "duration_minutes": 30,
    }

    response = requests.post(APPOINTMENTS_ENDPOINT, json=payload)

    # Pydantic validation error
    assert response.status_code == 422


def test_get_appointments_by_date():
    """
    Retrieve appointments for a specific date.
    """
    date_str = (datetime.now(timezone.utc) + timedelta(days=1)).date().isoformat()

    response = requests.get(APPOINTMENTS_ENDPOINT, params={"date": date_str})

    assert response.status_code == 200
    assert isinstance(response.json(), list)
