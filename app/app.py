"""Vehicle Service API - Flask implementation.

Implements the contract defined by the OpenAPI spec, the Vehicle Service
Collection, and the generated Python SDK. All responses are JSON.
"""
import os

from flask import Flask, jsonify, request

from models import Vehicle

# Mutable fields that may be set/updated by clients.
MUTABLE_FIELDS = ("nickName", "vin", "make", "model", "year", "miles")
# Attributes required when creating a vehicle.
REQUIRED_ATTRS = ("nickName", "vin", "make", "model", "year")

# Seed data so GET works immediately.
SEED_VEHICLE = {
    "id": 1,
    "nickName": "The Lisa Marie",
    "vin": "4M2DV11W4RDJ53329",
    "make": "Mercury",
    "model": "Villager",
    "year": "1994",
    "miles": 159864,
}


def create_app():
    app = Flask(__name__)

    # In-memory store keyed by integer id, with an auto-incrementing counter.
    store = {}
    counter = {"next_id": 1}

    def _add_vehicle(data):
        """Create and store a Vehicle, assigning the next id."""
        vehicle = Vehicle(
            id=counter["next_id"],
            nickName=data["nickName"],
            vin=data["vin"],
            make=data["make"],
            model=data["model"],
            year=data["year"],
            miles=data.get("miles", 0),
        )
        store[vehicle.id] = vehicle
        counter["next_id"] += 1
        return vehicle

    # Seed one sample vehicle.
    seed = Vehicle(**SEED_VEHICLE)
    store[seed.id] = seed
    counter["next_id"] = seed.id + 1

    @app.route("/vehicles", methods=["GET"])
    def list_vehicles():
        return jsonify([v.to_dict() for v in store.values()]), 200

    @app.route("/vehicles", methods=["POST"])
    def create_vehicle():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"message": "Bad request body."}), 400

        # Report the first missing required attribute.
        for attr in REQUIRED_ATTRS:
            if attr not in data or data[attr] in (None, ""):
                return (
                    jsonify(
                        {"message": f"Request body missing required attribute: {attr}"}
                    ),
                    400,
                )

        # Reject duplicate VIN.
        for existing in store.values():
            if existing.vin == data["vin"]:
                return (
                    jsonify(
                        {
                            "message": (
                                f"Vehicle with VIN {data['vin']} already exists. "
                                f"Existing vehicle ID: {existing.id}"
                            )
                        }
                    ),
                    409,
                )

        vehicle = _add_vehicle(data)
        return jsonify(vehicle.to_dict()), 201

    @app.route("/vehicles/<int:vehicle_id>", methods=["GET"])
    def get_vehicle(vehicle_id):
        vehicle = store.get(vehicle_id)
        if vehicle is None:
            return (
                jsonify({"message": f"Vehicle with id: {vehicle_id} not found."}),
                404,
            )
        return jsonify(vehicle.to_dict()), 200

    @app.route("/vehicles/<int:vehicle_id>", methods=["PATCH"])
    def update_vehicle(vehicle_id):
        vehicle = store.get(vehicle_id)
        if vehicle is None:
            return (
                jsonify({"message": f"Vehicle with id: {vehicle_id} not found."}),
                404,
            )

        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"message": "Bad request body."}), 400

        for field_name in MUTABLE_FIELDS:
            if field_name in data:
                setattr(vehicle, field_name, data[field_name])

        return jsonify(vehicle.to_dict()), 200

    @app.route("/vehicles/<int:vehicle_id>", methods=["DELETE"])
    def delete_vehicle(vehicle_id):
        if vehicle_id not in store:
            return (
                jsonify({"message": f"Vehicle with id: {vehicle_id} not found."}),
                404,
            )
        del store[vehicle_id]
        return "", 204

    @app.errorhandler(Exception)
    def handle_unexpected_error(exc):
        # Preserve HTTP exceptions (e.g. 404 for unknown routes) raised by Flask.
        from werkzeug.exceptions import HTTPException

        if isinstance(exc, HTTPException):
            return exc
        return jsonify({"message": "An unexpected error occurred."}), 500

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
