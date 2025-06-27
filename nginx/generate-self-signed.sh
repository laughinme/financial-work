#!/usr/bin/env bash
set -e
mkdir -p ssl
openssl req -x509 -nodes -days 365 \
    -newkey rsa:2048 \
    -keyout ssl/server.key \
    -out ssl/server.crt \
    -subj "/CN=localhost"
echo "Self-signed certificate generated in ./nginx/ssl" 
