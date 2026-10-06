# Vehicle Service API — Python Implementation

A Flask implementation of the **Vehicle Service API**, generated from the Postman
OpenAPI spec (`postman/specs/Vehicle Service API/index.yaml`), the
**Vehicle Service Collection**, and the generated Python SDK.

It manages a fleet of vehicle records and exposes a single `vehicles` resource
following standard HTTP semantics.

## Project layout

```
app/
├── app.py            # Flask application factory + routes
├── models.py         # Vehicle dataclass
├── test_app.py       # pytest suite (contract tests for every status code)
├── requirements.txt  # Flask + pytest
└── README.md
```

## Vehicle object

| Field    | Type   | Notes                     |
|----------|--------|---------------------------|
| id       | int    | Server-assigned           |
| nickName | string | Required on create        |
| vin      | string | Required on create, unique|
| make     | string | Required on create        |
| model    | string | Required on create        |
| year     | string | Required on create        |
| miles    | int    | Optional / mutable        |

## Endpoints

| Method | Path             | Success | Errors                        |
|--------|------------------|---------|-------------------------------|
| GET    | `/vehicles`      | 200     | 500                           |
| POST   | `/vehicles`      | 201     | 400 (missing attr), 409 (dup VIN), 500 |
| GET    | `/vehicles/<id>` | 200     | 404, 500                      |
| PATCH  | `/vehicles/<id>` | 200     | 400 (bad body), 404, 500      |
| DELETE | `/vehicles/<id>` | 204     | 404, 500                      |

Error responses use the shape `{"message": "<description>"}`.

## Setup & run

From the `app/` directory:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run the server (defaults to port 8080; override with PORT)
python app.py
# PORT=9000 python app.py
```

The server listens on `http://localhost:8080`. It starts with one seeded
vehicle so `GET /vehicles` returns data immediately.

## Run the tests

```bash
source .venv/bin/activate
python -m pytest -q
```

All contract tests cover each documented status code (200, 201, 204, 400, 404, 409).

## Try it

```bash
# List all vehicles
curl http://localhost:8080/vehicles

# Retrieve one
curl http://localhost:8080/vehicles/1

# Create a vehicle
curl -X POST http://localhost:8080/vehicles \
  -H "Content-Type: application/json" \
  -d '{"nickName":"Red Rocket","vin":"JN8AZ2KR1AT169594","make":"Nissan","model":"Cube","year":"2010"}'

# Update mileage
curl -X PATCH http://localhost:8080/vehicles/1 \
  -H "Content-Type: application/json" \
  -d '{"miles":160000}'

# Delete
curl -X DELETE http://localhost:8080/vehicles/1
```

## Point Postman at this app

Set the `baseUrl` variable in your Postman environment to
`http://localhost:8080`, then run the **Vehicle Service Collection** against
this local implementation.
