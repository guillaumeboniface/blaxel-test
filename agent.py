"""Toy LiveKit voice agent — uses OpenAI for STT, LLM, and TTS."""

import logging

from livekit.agents import AgentSession, Agent, cli, JobContext, AgentServer
from livekit.plugins import openai, silero

logger = logging.getLogger("toy-voice-agent")
logger.setLevel(logging.INFO)


class ToyAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are a friendly voice assistant running inside a Blaxel sandbox. "
                "Keep your answers concise and cheerful. "
                "If the user asks what you are, explain you are a proof-of-concept "
                "LiveKit voice agent running in a lightweight cloud sandbox."
            ),
        )


server = AgentServer()


@server.rtc_session()
async def entrypoint(ctx: JobContext):
    await ctx.connect()

    session = AgentSession(
        stt=openai.STT(model="whisper-1"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai.TTS(model="tts-1", voice="alloy"),
        vad=silero.VAD.load(),
    )

    await session.start(
        room=ctx.room,
        agent=ToyAssistant(),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    cli.run_app(server)
