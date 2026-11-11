$ErrorActionPreference = "Stop"

if (Test-Path "generated_service") {
    Remove-Item -Recurse -Force "generated_service"
}

openapi-generator-cli generate -i api.yaml -g python-flask -o generated_service
