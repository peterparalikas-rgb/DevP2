# VehicleServiceCollectionSdk Python SDK 1.0.0

Welcome to the VehicleServiceCollectionSdk SDK documentation. This guide will help you get started with integrating and using the VehicleServiceCollectionSdk SDK in your project.

## Versions

- SDK version: `1.0.0`

## About the API

# Vehicle Service API — Getting Started Guide

## Overview & Purpose

The **Vehicle Service API** is a RESTful service for managing a fleet of vehicle records. It lets you create, retrieve, update, and delete vehicles, each described by attributes such as a nickname, VIN, make, model, year, and mileage. The API is intentionally simple and resource-oriented, exposing a single `vehicles` resource that follows standard HTTP semantics (GET/POST/PATCH/DELETE), making it easy to integrate into inventory, dealership, maintenance, or telematics systems.

The intent of this API is to serve as the **single source of truth for vehicle records** — a lightweight backing service that other applications call to persist and read vehicle data without needing to know the underlying storage details.

### Typical End Users

- **Backend/Integration developers** building fleet, dealership, or inventory applications that need to persist vehicle data.
- **QA & Test engineers** validating vehicle workflows against mock or staging environments.
- **Frontend developers** who need a reliable contract (via the mock server) to build UIs before the backend is ready.
- **Automation / DevOps engineers** running the collection in monitors or CI pipelines to check service health.

### Common Use Cases

- Registering a new vehicle in a fleet or inventory system (**Create a vehicle**).
- Listing the full fleet for dashboards or reports (**Get all vehicles**).
- Looking up a single vehicle's details by ID (**Retrieve a vehicle**).
- Updating mutable attributes such as mileage or nickname (**Update a collection / vehicle**).
- Retiring or removing a vehicle from the fleet (**Delete a vehicle**).
- Front-end prototyping and contract testing against the Postman mock server.

---

## 1. Authenticating API Requests (Step by Step)

This collection uses an **API key** that is stored securely in the Postman Vault and referenced as `{{vault:apiKey}}`.

1. Open the **Vehicle Service Collection** in the sidebar and click its name to open collection settings.
2. Go to the **Authorization** tab for the collection.
3. Choose an auth type that matches the service — for an API key, select **API Key** (or **Bearer Token** if the service expects a bearer header).
4. In the **Value** field, reference the vaulted secret instead of pasting the raw key: `{{vault:apiKey}}`.
   - For API Key auth: set **Key** to the header name the service expects (for example `X-API-Key`), **Value** to `{{vault:apiKey}}`, and **Add to** = `Header`.
   - For Bearer auth: set **Token** to `{{vault:apiKey}}`.
5. Leave each individual request's Authorization set to **Inherit auth from parent** so every request automatically uses the collection-level credential. This means you configure the key in exactly one place.
6. Send any request (for example **Get all vehicles**). A `200` response confirms authentication is working; a `401`/`403` means the key is missing or invalid (see the Error Handling section).

> Tip: Never hardcode the raw API key into a request, header, or environment value that is synced. Always reference `{{vault:apiKey}}` so the secret stays local and private.

---

## 2. Managing Multiple Environments

Environments let you point the same requests at different servers (mock, staging, production) by swapping variable values instead of editing each request.

**Key variable:** `baseUrl` — the root URL of the API. Every request is built as `{{baseUrl}}/vehicles`.

Step by step:

1. In the left sidebar, open the **Environments** tab.
2. The workspace ships with a **Mock Environment** where `baseUrl` points to the Postman mock server (`https://086a6e23-004a-4429-b4ee-8889b49190ef.mock.pstmn.io`).
3. To add another environment (e.g. Staging or Production), click **+** to create a new environment, add a variable named `baseUrl`, and set its **Current Value** to that environment's host (for example `https://staging.api.vehicle-service.com`).
4. Use the **environment selector** (top-right of the app) to switch the active environment. All requests using `{{baseUrl}}` instantly target the selected environment — no request edits needed.
5. Keep secrets (like the API key) out of environments — use the Vault instead (see next section). Use environments only for non-secret, environment-specific config such as URLs.

> Best practice: Use the **Current Value** (local, not synced) for anything sensitive or machine-specific, and the **Initial Value** (synced to the team) only for safe, shareable defaults.

---

## 3. Securely Storing API Keys in the Vault

The **Postman Vault** stores secrets locally on your machine; vault values are never synced to Postman's servers or shared with your team.

Step by step:

1. At the bottom-left of the Postman app, click the **Vault** icon.
2. Unlock the Vault (set a Vault key / password the first time if prompted).
3. Click **Add secret**. Set the **Name** to `apiKey` and paste your real API key as the **Value**. Save.
4. Reference it anywhere in the collection — in auth, headers, or body — using the syntax `{{vault:apiKey}}`.
5. Because the collection authorization already uses `{{vault:apiKey}}`, every inheriting request is now authenticated with your private key with nothing sensitive stored in the collection or environment.

> Why this matters: Vault secrets never leave your device. This prevents accidental leakage of credentials through synced collections, environments, or shared workspaces.

---

## 4. Handling Common Errors (by Status Code)

Each request in this collection includes saved **examples** that show the exact response shape for both success and error cases. Use this table to diagnose and respond to failures.

| Status                                 | Meaning                 | Likely Cause                                                | How to Handle                                                                                                                  |
| -------------------------------------- | ----------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **200 OK**                             | Success                 | Request succeeded (GET/PATCH)                               | Parse and use the returned vehicle data.                                                                                       |
| **201 Created**                        | Resource created        | A vehicle was successfully created (POST)                   | Store the returned `id` for later retrieval/updates.                                                                           |
| **204 No Content**                     | Success, no body        | Vehicle successfully deleted (DELETE)                       | No body is returned — treat as success.                                                                                        |
| **400 Bad Request**                    | Invalid input           | Missing required attribute or malformed JSON body           | Check the request body against the required schema (e.g. `vin`, `make`, `model`). Fix the field named in the error and resend. |
| **401 / 403 Unauthorized / Forbidden** | Auth failure            | Missing, invalid, or expired API key                        | Verify `{{vault:apiKey}}` is set in the Vault and the collection Authorization is configured correctly.                        |
| **404 Not Found**                      | Resource missing        | The `:id` path parameter does not match any vehicle         | Confirm the `id` exists (run **Get all vehicles** first) and that `baseUrl` points to the right environment.                   |
| **409 Conflict**                       | Duplicate resource      | Creating a vehicle that already exists (e.g. duplicate VIN) | Retrieve the existing vehicle instead of recreating it, or change the conflicting unique field.                                |
| **500 Internal Server Error**          | Unexpected server error | A fault on the server side                                  | Retry with backoff; if it persists, the issue is server-side — check service health and report it.                             |

> Tip: Open the matching example (e.g. **400 - Missing required attribute**, **404 - Not found**, **409 - Vehicle already exists**) under each request to see the precise error payload before writing client-side handling.

---

## 5. Parameter Types & Contextual Information

This API uses three categories of parameters.

### Path Parameters

- `:id` — Used in **Retrieve**, **Update**, and **Delete** requests as `{{baseUrl}}/vehicles/:id`. This is the unique identifier of the vehicle. Set its value in the request's **Path Variables** section. Required for any single-vehicle operation.

### Variables

- `baseUrl` _(string, required)_ — The API host. Resolved from the active environment or collection. Example: a mock host or a staging/production URL.
- `vault:apiKey` _(secret, required)_ — The API credential, pulled from the Vault.

### Request Body (JSON) — for Create and Update

Sent with `Content-Type: application/json`. Fields for a vehicle:

| Field      | Type   | Description                            | Example               |
| ---------- | ------ | -------------------------------------- | --------------------- |
| `nickName` | string | Friendly name for the vehicle          | `"The Lisa Marie"`    |
| `vin`      | string | Vehicle Identification Number (unique) | `"4M2DV11W4RDJ53329"` |
| `make`     | string | Manufacturer                           | `"Mercury"`           |
| `model`    | string | Model name                             | `"Villager"`          |
| `year`     | string | Model year                             | `"1994"`              |
| `miles`    | number | Odometer reading                       | `159864`              |

### Headers

- `Content-Type: application/json` — required on requests that send a body (Create, Update).
- `Accept: application/json` — tells the server to return JSON.

---

## Quick Start Checklist

1. Add your API key to the Vault as `apiKey`.
2. Confirm the collection Authorization references `{{vault:apiKey}}`.
3. Select the **Mock Environment** (or your own) so `baseUrl` resolves.
4. Send **Get all vehicles** — a `200` confirms you're set up correctly.
5. Try **Create a vehicle**, then **Retrieve**, **Update**, and **Delete** using the returned `id`.

## Table of Contents

- [Setup & Configuration](#setup--configuration)
  - [Supported Language Versions](#supported-language-versions)
  - [Installation](#installation)
- [Authentication](#authentication)
  - [API Key Authentication](#api-key-authentication)
- [Setting a Custom Timeout](#setting-a-custom-timeout)
- [Sample Usage](#sample-usage)
- [Async Usage](#async-usage)
- [Services](#services)
- [Models](#models)

# Setup & Configuration

## Supported Language Versions

This SDK is compatible with the following versions: `Python >= 3.9`

## Installation

To get started with the SDK, we recommend installing using `pip`:

```bash
pip install vehicle_service_collection_sdk
```

If you are using Python 3, you can use `pip3` instead:

```bash
pip3 install vehicle_service_collection_sdk
```

## Disabling Redirects

By default, the SDK follows HTTP redirects (3xx responses) automatically. Pass
`follow_redirects=False` to get the redirect response back as-is instead:

```python
client = VehicleServiceCollectionSdk(follow_redirects=False)
```

This can also be changed later with `client.set_follow_redirects(False)`.

## Logging

The SDK is silent by default. Pass a standard library `logging.Logger` as `logger` to log
every outgoing request and its response (method, URL, status, and duration):

```python
import logging

logger = logging.getLogger("VehicleServiceCollectionSdk")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

client = VehicleServiceCollectionSdk(logger=logger)
```

This can also be changed later with `client.set_logging(logger)`.

`Authorization` and `Cookie` header values are always redacted in logged output, regardless
of the logger's own configuration.

## Authentication

### API Key Authentication

The VehicleServiceCollectionSdk API uses API keys as a form of authentication. An API key is a unique identifier used to authenticate a user, developer, or a program that is calling the API.

#### Setting the API key

When you initialize the SDK, you can set the API key as follows:

```py
VehicleServiceCollectionSdk(
    api_key="YOUR_API_KEY",
    timeout=10
)
```

If you need to set or update the API key after initializing the SDK, you can use:

```py
sdk.set_api_key("YOUR_API_KEY")
```

## Setting a Custom Timeout

You can set a custom timeout for the SDK's HTTP requests as follows:

```py
from vehicle_service_collection_sdk import VehicleServiceCollectionSdk

sdk = VehicleServiceCollectionSdk(timeout=10)
```

# Sample Usage

Below is a comprehensive example demonstrating how to authenticate and call a simple endpoint:

```py
from vehicle_service_collection_sdk import VehicleServiceCollectionSdk, Environment

sdk = VehicleServiceCollectionSdk(
    api_key="YOUR_API_KEY",
    base_url=Environment.DEFAULT.value,
    timeout=10
)

result = sdk.vehicle_service_collection_sdk.get_all_vehicles()

print(result)

```

# Async Usage

The SDK includes an Async Client for making asynchronous API requests. This is useful for applications that need non-blocking operations, like web servers or apps with a graphical user interface.

```py
import asyncio
from vehicle_service_collection_sdk import VehicleServiceCollectionSdkAsync, Environment
from vehicle_service_collection_sdk.models import CreateAVehicleRequest

sdk = VehicleServiceCollectionSdkAsync(
    api_key="YOUR_API_KEY",
    base_url=Environment.DEFAULT.value,
    timeout=10
)


request_body = CreateAVehicleRequest(
    nick_name="The Lisa Marie",
    vin="4M2DV11W4RDJ53329",
    make="Mercury",
    model="Villager",
    year="1994",
    miles=159864
)

async def main():
  result = await sdk.vehicle_service_collection_sdk.create_a_vehicle(request_body=request_body)
  print(result)

asyncio.run(main())
```

## Services

The SDK provides various services to interact with the API.

<details>
<summary>Below is a list of all available services with links to their detailed documentation:</summary>

| Name                                                                                               |
| :------------------------------------------------------------------------------------------------- |
| [VehicleServiceCollectionSdkService](documentation/services/VehicleServiceCollectionSdkService.md) |

</details>

## Models

The SDK includes several models that represent the data structures used in API requests and responses. These models help in organizing and managing the data efficiently.

<details>
<summary>Below is a list of all available models with links to their detailed documentation:</summary>

| Name                                                                   | Description |
| :--------------------------------------------------------------------- | :---------- |
| [CreateAVehicleRequest](documentation/models/CreateAVehicleRequest.md) |             |

</details>
