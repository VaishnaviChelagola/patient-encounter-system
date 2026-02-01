from datetime import datetime


def test_create_and_get_patient(client):
    # Create patient
    response = client.post(
        "/patients",
        json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com",
            "phone_number": "1234567890",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "Alice"
    patient_id = data["id"]

    # Get patient
    response = client.get(f"/patients/{patient_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "alice@example.com"
