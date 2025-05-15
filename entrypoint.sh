#!/bin/sh

echo "Starting service with APP_TARGET=$APP_TARGET"

if [ "$APP_TARGET" = "bot" ]; then
    python3 bot/main.py
else
    python3 backend/src/access_service/bootstrap/entrypoint/fast_api.py
fi
