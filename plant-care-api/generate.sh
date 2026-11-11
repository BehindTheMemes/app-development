#!/usr/bin/env bash
set -e

rm -rf generated_service
openapi-generator-cli generate -i api.yaml -g python-flask -o generated_service
