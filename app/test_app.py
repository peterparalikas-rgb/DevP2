"""Pytest suite for the Vehicle Service API."""
import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def _new_vehicle_payload(**overrides):
    payload = {
        "nickName": "Test Car",
        "vin": "1HGCM82633A004352",
        "make": "Honda",
        "model": "Accord",
        "year": "2003",
        "miles": 120000,
    }
    payload.update(overrides)
    return payload


def test_list_vehicles(client):
    resp = client.get("/vehicles")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["id"] == 1
    assert data[0]["nickName"] == "The Lisa Marie"


def test_create_success(client):
    resp = client.post("/vehicles", json=_new_vehicle_payload())
    assert resp.status_code == 201
    data = resp.get_json()
    assert isinstance(data["id"], int)
    assert data["nickName"] == "Test Car"
    assert data["vin"] == "1HGCM82633A004352"
    assert data["miles"] == 120000


def test_create_missing_attribute(client):
    payload = _new_vehicle_payload()
    del payload["make"]
    resp = client.post("/vehicles", json=payload)
    assert resp.status_code == 400
    assert resp.get_json() == {
        "message": "Request body missing required attribute: make"
    }


def test_create_duplicate_vin(client):
    resp = client.post("/vehicles", json=_new_vehicle_payload(vin="4M2DV11W4RDJ53329"))
    assert resp.status_code == 409
    assert resp.get_json() == {
        "message": "Vehicle with VIN 4M2DV11W4RDJ53329 already exists. "
        "Existing vehicle ID: 1"
    }


def test_retrieve_found(client):
    resp = client.get("/vehicles/1")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == 1
    assert data["vin"] == "4M2DV11W4RDJ53329"


def test_retrieve_not_found(client):
    resp = client.get("/vehicles/9999")
    assert resp.status_code == 404
    assert resp.get_json() == {"message": "Vehicle with id: 9999 not found."}


def test_patch_success(client):
    resp = client.patch("/vehicles/1", json={"nickName": "Renamed", "miles": 200000})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == 1
    assert data["nickName"] == "Renamed"
    assert data["miles"] == 200000


def test_patch_not_found(client):
    resp = client.patch("/vehicles/9999", json={"nickName": "Nope"})
    assert resp.status_code == 404
    assert resp.get_json() == {"message": "Vehicle with id: 9999 not found."}


def test_delete_success(client):
    created = client.post("/vehicles", json=_new_vehicle_payload(vin="JH4KA8260MC000000"))
    new_id = created.get_json()["id"]
    resp = client.delete(f"/vehicles/{new_id}")
    assert resp.status_code == 204
    assert resp.data == b""


def test_delete_not_found(client):
    resp = client.delete("/vehicles/9999")
    assert resp.status_code == 404
    assert resp.get_json() == {"message": "Vehicle with id: 9999 not found."}
