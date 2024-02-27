#!/bin/bash

BASE_URL="http://localhost:8000/api/v1"

LOGIN_URL="$BASE_URL/login"

USERNAME="your_username"
PASSWORD="your_password"

SENSOR_ID=2

# Endpoint URIs
CREATE_ENDPOINT="$BASE_URL/sensor-readings/?sensor_id=$SENSOR_ID" # Adjusted to include query parameter for sensor_id
READ_ENDPOINT_BASE="$BASE_URL/sensor-readings/"
SENSOR_READINGS_ENDPOINT="$BASE_URL/sensors/$SENSOR_ID/readings/"
UPDATE_ENDPOINT_BASE="$BASE_URL/sensor-readings/"
DELETE_ENDPOINT_BASE="$BASE_URL/sensor-readings/"

# Login and get token
echo "Logging in to obtain token..."
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


# Example: Create a new sensor reading for sensor 2 with Authorization
echo "Creating a new sensor reading for sensor $SENSOR_ID with Authorization..."
CREATE_RESPONSE=$(curl -s -X POST "$CREATE_ENDPOINT" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d "{\"value\": 23.5, \"timestamp\": \"$(date --iso-8601=seconds)\"}")
echo "Create response: $CREATE_RESPONSE"