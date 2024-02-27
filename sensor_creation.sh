#!/bin/bash

# Define credentials, endpoints, and sensor data
USERNAME="your_username"
PASSWORD="your_password"
LOGIN_URL="http://localhost:8000/token"
SENSORS_URL="http://localhost:8000/api/v1/sensors/"
PLANTS_URL="http://localhost:8000/api/v1/plants/"
PLANT_ID="1"  # Assume you have this from previous operations or setup
SENSOR_TYPE="moisture"
SENSOR_UNIT="%"

# Login to get the token
LOGIN_RESPONSE=$(curl -s -X 'POST' \
  "$LOGIN_URL" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d "username=$USERNAME&password=$PASSWORD")

# Extract token from the login response
TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access_token')

if [ -z "$TOKEN" ] || [ "$TOKEN" == "null" ]; then
  echo "Failed to obtain token."
  exit 1
fi

echo "Token obtained successfully. Token: $TOKEN"

# Create a sensor
echo "Attempting to create a sensor..."
CREATE_SENSOR_RESPONSE=$(curl -s -X 'POST' \
  "${SENSORS_URL}" \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{
  \"plant_id\": $PLANT_ID,
  \"type\": \"$SENSOR_TYPE\",
  \"unit\": \"$SENSOR_UNIT\"
}")

echo "Create sensor response: $CREATE_SENSOR_RESPONSE"

# Extract sensor ID from the create sensor response
SENSOR_ID=$(echo $CREATE_SENSOR_RESPONSE | jq -r '.id')

if [ -z "$SENSOR_ID" ] || [ "$SENSOR_ID" == "null" ]; then
  echo "Failed to create sensor or obtain sensor ID."
  exit 1
fi

echo "Sensor created successfully. Sensor ID: $SENSOR_ID"

# Read a sensor
echo "Reading sensor with ID $SENSOR_ID..."
READ_SENSOR_RESPONSE=$(curl -s -X 'GET' \
  "${SENSORS_URL}${SENSOR_ID}" \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $TOKEN")

echo "Read sensor response: $READ_SENSOR_RESPONSE"

# Read sensors by plant
echo "Reading sensors for plant ID $PLANT_ID..."
READ_SENSORS_PLANT_RESPONSE=$(curl -s -X 'GET' \
  "${PLANTS_URL}${PLANT_ID}/sensors/" \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $TOKEN")

echo "Read sensors by plant response: $READ_SENSORS_PLANT_RESPONSE"

# Update a sensor
echo "Updating sensor with ID $SENSOR_ID..."
UPDATE_SENSOR_RESPONSE=$(curl -s -X 'PUT' \
  "${SENSORS_URL}${SENSOR_ID}" \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{
  \"type\": \"$SENSOR_TYPE\",
  \"unit\": \"$SENSOR_UNIT\"
}")

echo "Update sensor response: $UPDATE_SENSOR_RESPONSE"

# Delete a sensor
echo "Deleting sensor with ID $SENSOR_ID..."
DELETE_SENSOR_RESPONSE=$(curl -s -X 'DELETE' \
  "${SENSORS_URL}${SENSOR_ID}" \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $TOKEN")

echo "Delete sensor response: $DELETE_SENSOR_RESPONSE"
