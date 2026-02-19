#!/bin/bash
set -e

# Start the Blaxel sandbox API (required)
/usr/local/bin/sandbox-api &

# Wait for sandbox API to be ready
while ! nc -z 127.0.0.1 8080; do
  sleep 0.1
done

echo "==> Starting token server on :8888..."
python3 /app/token_server.py &
TOKEN_PID=$!

echo "==> Starting voice agent worker..."
python3 /app/agent.py start &
AGENT_PID=$!

echo "==> All services running (token=$TOKEN_PID, agent=$AGENT_PID)"

wait -n $TOKEN_PID $AGENT_PID
