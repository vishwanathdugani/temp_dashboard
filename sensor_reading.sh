#!/bin/bash

# Base URL of the FastAPI application
BASE_URL="http://localhost:8000/api/v1"

# Sensor ID for demonstration
SENSOR_ID=2

# Endpoint URIs
CREATE_ENDPOINT="$BASE_URL/sensor-readings/?sensor_id=$SENSOR_ID" # Adjusted to include query parameter for sensor_id
READ_ENDPOINT_BASE="$BASE_URL/sensor-readings/"
SENSOR_READINGS_ENDPOINT="$BASE_URL/sensors/$SENSOR_ID/readings/"
UPDATE_ENDPOINT_BASE="$BASE_URL/sensor-readings/"
DELETE_ENDPOINT_BASE="$BASE_URL/sensor-readings/"

# Create a new sensor reading for sensor 2
echo "Creating a new sensor reading for sensor $SENSOR_ID..."
CREATE_RESPONSE=$(curl -s -X POST "$CREATE_ENDPOINT" -H "Content-Type: application/json" -d "{\"value\": 23.5, \"timestamp\": \"$(date --iso-8601=seconds)\"}")
echo "Create response: $CREATE_RESPONSE"

# Extract the ID of the created sensor reading
READING_ID=$(echo $CREATE_RESPONSE | jq '.id')
echo "Created reading ID: $READING_ID"

# Verify READING_ID is not null or empty
if [ "$READING_ID" == "null" ] || [ -z "$READING_ID" ]; then
  echo "Failed to extract reading ID from create response."
  exit 1
fi


# Retrieve the created sensor reading
echo "Retrieving the created sensor reading..."
READ_RESPONSE=$(curl -s -X GET "${READ_ENDPOINT_BASE}${READING_ID}")
echo "Read response: $READ_RESPONSE"

# Update the created sensor reading
echo "Updating the created sensor reading..."
UPDATE_RESPONSE=$(curl -s -X PUT "${UPDATE_ENDPOINT_BASE}${READING_ID}" -H "Content-Type: application/json" -d "{\"value\": 24.5, \"timestamp\": \"$(date --iso-8601=seconds)\"}")
echo "Update response: $UPDATE_RESPONSE"

# Retrieve all readings for sensor 2
echo "Retrieving all readings for sensor $SENSOR_ID..."
ALL_READINGS_RESPONSE=$(curl -s -X GET "${SENSOR_READINGS_ENDPOINT}")
echo "All readings for sensor $SENSOR_ID: $ALL_READINGS_RESPONSE"

# Delete the created sensor reading
echo "Deleting the created sensor reading..."
DELETE_RESPONSE=$(curl -s -X DELETE "${DELETE_ENDPOINT_BASE}${READING_ID}")
echo "Delete response: $DELETE_RESPONSE"
