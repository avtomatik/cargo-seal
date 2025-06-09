# Prompt the user for the file path
$filePath = Read-Host "Enter the full path to the Excel Declaration Form"

# Validate file existence
if (-Not (Test-Path $filePath)) {
    Write-Host "Error: File '$filePath' not found." -ForegroundColor Red
    exit 1
}

# Define the API endpoint
$apiUrl = "http://localhost:8000/api/coverage/push/"

# Prepare the form data
$form = @{
    file = Get-Item $filePath
}

# Send the request
try {
    $response = Invoke-WebRequest -Uri $apiUrl -Method Post -Form $form -ContentType "multipart/form-data"
    Write-Host "Upload successful. Server responded with status code $($response.StatusCode)." -ForegroundColor Green
} catch {
    Write-Host "Upload failed: $($_.Exception.Message)" -ForegroundColor Red
}
