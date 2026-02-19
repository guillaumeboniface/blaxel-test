FROM python:3.12-slim AS base

# ── System deps ──────────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
        netcat-openbsd ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# ── Inject Blaxel sandbox API ────────────────────────────────────────────────
COPY --from=ghcr.io/blaxel-ai/sandbox:latest /sandbox-api /usr/local/bin/sandbox-api

# ── Python dependencies ─────────────────────────────────────────────────────
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Download Silero VAD model ahead of time ──────────────────────────────────
RUN python3 -c "from livekit.plugins.silero import VAD; VAD.load()" || true

# ── Application code ─────────────────────────────────────────────────────────
COPY agent.py token_server.py client.html ./
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8888

ENTRYPOINT ["/entrypoint.sh"]
