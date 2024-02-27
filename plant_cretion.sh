#!/bin/bash

# Define credentials, endpoints, and plant data
USERNAME="your_username"
PASSWORD="your_password"
LOGIN_URL="http://localhost:8000/token"
PLANTS_URL="http://localhost:8000/api/v1/plants/"
PLANT_NAME="Unique Plant Name"
PLANT_LOCATION="Unique Plant Location"

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

# Attempt to create a plant with the active token
echo "Attempting to create a plant..."
CREATE_PLANT_RESPONSE=$(curl -s -X 'POST' \
  "$PLANTS_URL" \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{
  \"name\": \"$PLANT_NAME\",
  \"location\": \"$PLANT_LOCATION\"
}")

# Extract HTTP status and Plant ID from the creation attempt
CREATE_PLANT_STATUS=$(echo "$CREATE_PLANT_RESPONSE" | jq -r '.status')
PLANT_ID=$(echo "$CREATE_PLANT_RESPONSE" | jq -r '.id')

if [ -z "$PLANT_ID" ] || [ "$PLANT_ID" == "null" ]; then
  echo "Failed to create plant. Response: $CREATE_PLANT_RESPONSE"
  exit 1
else
  echo "Plant created successfully with ID: $PLANT_ID"
fi

# Use the token to list all plants
echo "Listing all plants..."
LIST_PLANTS_RESPONSE=$(curl -s -X 'GET' \
  "$PLANTS_URL" \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $TOKEN")

echo "Plants: $LIST_PLANTS_RESPONSE"

# Reading by ID
echo "Reading plant with ID $PLANT_ID..."
READ_PLANT_RESPONSE=$(curl -s -X 'GET' \
  "${PLANTS_URL}${PLANT_ID}" \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $TOKEN")

echo "Plant Details: $READ_PLANT_RESPONSE"

# Attempt to update a specific plant
echo "Updating plant with ID $PLANT_ID..."
UPDATE_PLANT_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X 'PUT' \
  "${PLANTS_URL}${PLANT_ID}" \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{
    \"name\": \"${PLANT_NAME} Updated\",
    \"location\": \"${PLANT_LOCATION} Updated\"
  }")

if [ "$UPDATE_PLANT_RESPONSE" -eq "200" ]; then
  echo "Plant updated successfully."
else
  echo "Failed to update plant. HTTP status: $UPDATE_PLANT_RESPONSE"
fi

# Attempt to delete a specific plant
echo "Deleting plant with ID $PLANT_ID..."
DELETE_PLANT_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X 'DELETE' \
  "${PLANTS_URL}${PLANT_ID}" \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $TOKEN")

if [ "$DELETE_PLANT_RESPONSE" -eq "200" ]; then
  echo "Plant deleted successfully."
else
  echo "Failed to delete plant. HTTP status: $DELETE_PLANT_RESPONSE"
fi
