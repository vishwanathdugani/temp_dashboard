# IoT Dashboard API

This repository contains the backend API for the IoT Dashboard, built using FastAPI. It provides endpoints to manage users, devices, and temperature readings.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Temperature Generator](#temperature-generator)
3. [Database Initialization](#database-initialization)
4. [Testing](#testing)
5. [API Endpoints](#api-endpoints)

## Getting Started

To set up the project, you'll need Docker and Docker Compose installed on your machine.

### Steps:

1. **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd <repository-dir>
    ```

2. **Build and run the application with Docker Compose:**

    ```bash
    docker-compose up -d
    ```

    This command will set up two services:

    - `db`: A PostgreSQL database.
    - `web`: The FastAPI application.

3. Once the services are up, you can access the FastAPI application at `http://localhost:8000`.

## Temperature Generator

Included in the codebase is a script that simulates temperature readings for various devices. It randomly selects a device ID and generates a random temperature reading for it, which is then published to an MQTT broker. This simulates real-world devices sending temperature readings to the backend.

## Database Initialization

The `init.sql` file contains the schema for the database. It sets up the necessary tables for users, devices, and temperature readings. This schema is crucial for the correct functioning of the backend API.

## Testing

Tests are written using `pytest`. To run the tests and generate an HTML report:

```bash
pytest tests.py --html=report.html
```

After running the tests, you can view the detailed report by opening the `report.html` file in your browser.

## API Endpoints

The API provides various endpoints:

- **Users:**
    - Register a new user.
    - Authenticate and get an access token.

- **Devices:**
    - Register a new device.
    - List all devices owned by an authenticated user.

- **Temperature:**
    - Add a new temperature reading.
    - Get the latest temperature reading for a device.
    - List all temperature readings for a device.
    - List temperature readings based on device ID or device name.

For detailed API documentation and to try out the endpoints, navigate to `http://localhost:8000/docs` in your browser.
