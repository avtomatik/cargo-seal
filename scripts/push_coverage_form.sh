#!/bin/bash

# Prompt for file path
read -rp "Enter the path to the Excel Declaration Form: " FILE_PATH

# Check if the file exists
if [[ ! -f "$FILE_PATH" ]]; then
  echo "Error: File '$FILE_PATH' not found."
  exit 1
fi

# Define the API endpoint
API_URL="http://localhost:8000/api/coverage/push/"

# Perform the upload using curl
curl -X POST -F "file=@${FILE_PATH};type=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" "$API_URL"
