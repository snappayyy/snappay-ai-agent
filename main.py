from fastapi import FastAPI, Request
from vocode.streaming.agent import ChatGPTAgent
from vocode.streaming.output_device.twilio import TwilioPhoneOutput
from vocode.streaming.input_device.twilio import TwilioInput
from vocode.streaming.pipeline import Pipeline
from vocode.streaming.models import (
    ChatGPTAgentConfig, WhisperTranscriberConfig,
    ElevenLabsSynthesizerConfig, TwilioConfig
)

app = FastAPI()

@app.post("/start-call")
async def start_call(req: Request):
    body = await req.json()
    phone = body["phone"]
    name = body.get("name", "en bedrift")

    agent = ChatGPTAgent(ChatGPTAgentConfig(
        system_prompt=f"Du er en norsk AI-selger som ringer til {name} og forklarer SnapPay.",
        model_name="gpt-4o"
    ))

    pipeline = Pipeline(
        input_device=TwilioInput(TwilioConfig()),
        output_device=TwilioPhoneOutput(TwilioConfig(), ElevenLabsSynthesizerConfig(voice_id="EXAVITQu4vr4xnSDxMaL")),
        transcriber_config=WhisperTranscriberConfig(),
        agent=agent
    )

    pipeline.start(phone_number=phone)
    return {"status": "call_started"}