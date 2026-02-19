# LiveKit Voice Agent on Blaxel Sandbox

A proof-of-concept voice AI agent running in a [Blaxel](https://blaxel.ai) sandbox, using [LiveKit Cloud](https://cloud.livekit.io) for WebRTC media routing and OpenAI for the voice pipeline.

## Architecture

```
┌──────────┐   WebRTC (UDP)    ┌───────────────┐   WSS + WebRTC   ┌─────────────────────┐
│  Browser  │ ◄──────────────► │  LiveKit Cloud │ ◄──────────────► │   Blaxel Sandbox    │
│           │                  │  (SFU)         │                  │                     │
│  client   │   WSS signaling  │                │   outbound from  │  Agent worker       │
│  .html    │ ──────────────►  │                │   sandbox        │  (STT → LLM → TTS) │
└──────────┘                   └───────────────┘                   │  Token server       │
                                                                   └─────────────────────┘
```

- **LiveKit Cloud** handles WebRTC media routing (UDP) between the browser and the agent
- **Blaxel sandbox** runs the agent worker and a small token server
- **Browser** connects to LiveKit Cloud for audio, and to the sandbox's token server for authentication

The agent connects **outbound** from the sandbox to LiveKit Cloud, avoiding Blaxel's inbound HTTP-only proxy limitation.

## Voice pipeline

| Stage | Provider | Model |
|-------|----------|-------|
| VAD   | Silero   | Silero VAD |
| STT   | OpenAI   | Whisper-1 |
| LLM   | OpenAI   | GPT-4o-mini |
| TTS   | OpenAI   | TTS-1 (alloy) |

## Prerequisites

- [Blaxel CLI](https://docs.blaxel.ai) (`bl`) installed and authenticated
- [LiveKit Cloud](https://cloud.livekit.io) account (free tier works)
- [OpenAI API key](https://platform.openai.com/api-keys)
- Docker

## Setup

1. Clone and fill in your credentials in `blaxel.toml`:

```toml
[env]
LIVEKIT_URL = "wss://your-project.livekit.cloud"
LIVEKIT_API_KEY = "your-key"
LIVEKIT_API_SECRET = "your-secret"
OPENAI_API_KEY = "sk-your-key"
```

2. Deploy to Blaxel:

```bash
bl deploy
```

3. In the [Blaxel console](https://app.blaxel.ai), create a preview URL for port **8888** on your sandbox.

4. Open the preview URL in your browser and click **Connect**.

## Local testing

```bash
export LIVEKIT_URL=wss://your-project.livekit.cloud
export LIVEKIT_API_KEY=your-key
export LIVEKIT_API_SECRET=your-secret
export OPENAI_API_KEY=sk-your-key

make build
make run
# Open http://localhost:8888
```

## Project structure

```
├── Dockerfile          Python 3.12 + Blaxel sandbox-api
├── blaxel.toml         Blaxel sandbox template config
├── entrypoint.sh       Starts sandbox-api → token server → agent worker
├── agent.py            LiveKit voice agent (OpenAI STT/LLM/TTS + Silero VAD)
├── token_server.py     HTTP server: serves client UI + issues LiveKit JWTs
├── client.html         Browser UI for testing the voice agent
├── requirements.txt    Python dependencies
└── Makefile            Build/run/deploy shortcuts
```
