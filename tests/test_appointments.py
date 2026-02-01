from datetime import datetime, timedelta, timezone

FUTURE_TIME = datetime(2026, 2, 1, 10, 0, 0, tzinfo=timezone.utc)


def create_patient_and_doctor(client, suffix="1"):
    patient_res = client.post(
        "/patients",
        json={
            "first_name": "Test",
            "last_name": "Patient",
            "email": f"test{suffix}@patient.com",
            "phone_number": "1111111111",
        },
    )
    assert patient_res.status_code == 201
    patient_id = patient_res.json()["id"]

    doctor_res = client.post(
        "/doctors",
        json={
            "full_name": f"Dr. Test {suffix}",
            "specialization": "Dermatology",
        },
    )
    assert doctor_res.status_code == 201
    doctor_id = doctor_res.json()["id"]

    return patient_id, doctor_id


def test_create_appointment_no_conflict(client):
    patient_id, doctor_id = create_patient_and_doctor(client, "a")

    response = client.post(
        "/appointments",
        headers={"Content-Type": "application/json"},
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "scheduled_start": FUTURE_TIME.isoformat(),
            "duration_minutes": 30,
        },
    )

    assert response.status_code == 201, response.json()


def test_appointment_conflict(client):
    patient_id, doctor_id = create_patient_and_doctor(client, "b")

    first = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "scheduled_start": FUTURE_TIME.isoformat(),
            "duration_minutes": 60,
        },
    )
    assert first.status_code == 201, first.json()

    conflict = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "scheduled_start": (FUTURE_TIME + timedelta(minutes=30)).isoformat(),
            "duration_minutes": 30,
        },
    )

    assert conflict.status_code == 409, conflict.json()


def test_back_to_back_appointments(client):
    patient_id, doctor_id = create_patient_and_doctor(client, "c")

    first = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "scheduled_start": FUTURE_TIME.isoformat(),
            "duration_minutes": 30,
        },
    )
    assert first.status_code == 201, first.json()

    second = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "scheduled_start": (FUTURE_TIME + timedelta(minutes=30)).isoformat(),
            "duration_minutes": 30,
        },
    )

    assert second.status_code == 201, second.json()
