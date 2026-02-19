"""Tiny HTTP server that serves the test client and issues LiveKit tokens.

Endpoints:
  GET  /           → serves client.html
  GET  /token      → returns a JWT + LiveKit Cloud URL for joining a room
  GET  /health     → health check
"""

import os
import pathlib

from aiohttp import web
from livekit import api

LIVEKIT_API_KEY = os.environ["LIVEKIT_API_KEY"]
LIVEKIT_API_SECRET = os.environ["LIVEKIT_API_SECRET"]
LIVEKIT_URL = os.environ["LIVEKIT_URL"]
ROOM_NAME = "test-room"

CLIENT_HTML = pathlib.Path(__file__).parent / "client.html"


async def handle_index(request):
    return web.FileResponse(CLIENT_HTML)


async def handle_token(request):
    identity = request.query.get("identity", "web-user")
    token = (
        api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        .with_identity(identity)
        .with_name(identity)
        .with_grants(
            api.VideoGrants(
                room_join=True,
                room=ROOM_NAME,
            )
        )
        .to_jwt()
    )
    # Return the LiveKit Cloud URL so the client knows where to connect
    livekit_ws_url = LIVEKIT_URL.replace("https://", "wss://").replace("http://", "ws://")
    return web.json_response({"token": token, "room": ROOM_NAME, "url": livekit_ws_url})


async def handle_health(request):
    return web.json_response({"status": "ok"})


app = web.Application()
app.router.add_get("/", handle_index)
app.router.add_get("/token", handle_token)
app.router.add_get("/health", handle_health)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8888)
