def test_create_and_get_doctor(client):
    # Create doctor
    response = client.post(
        "/doctors",
        json={
            "full_name": "Dr. Bob",
            "specialization": "Cardiology",
            "is_active": True,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "Dr. Bob"
    doctor_id = data["id"]

    # Get doctor
    response = client.get(f"/doctors/{doctor_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["specialization"] == "Cardiology"
