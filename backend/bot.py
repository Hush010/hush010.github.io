import os
from dotenv import load_dotenv
from pipecat import Pipeline
from pipecat.transports import WebRTCTransport
from pipecat.context import SimpleContextManager
from pipecat.services.openai import OpenAILLMService
from pipecat.services.deepgram import DeepgramSTTService
from pipecat.services.cartesia import CartesiaTTSService

load_dotenv()

# Track how many turns have been spoken
turns = {"count": 0}

class LimitedContextManager(SimpleContextManager):
    def on_turn_end(self):
        turns["count"] += 1
        if turns["count"] >= 3:  # after 3 exchanges, exit
            print("Conversation limit reached, shutting down...")
            os._exit(0)

def make_pipeline():
    transport = WebRTCTransport()
    stt = DeepgramSTTService(api_key=os.getenv("DEEPGRAM_API_KEY"))
    llm = OpenAILLMService(api_key=os.getenv("OPENAI_API_KEY"))
    tts = CartesiaTTSService(api_key=os.getenv("CARTESIA_API_KEY"))

    context_mgr = LimitedContextManager(
        system_prompt="You are a friendly voice agent. Greet the user, ask one follow-up, then say goodbye."
    )

    pipeline = Pipeline([
        transport.input(),
        stt,
        context_mgr,
        llm,
        tts,
        transport.output(),
    ])

    return pipeline

if __name__ == "__main__":
    pipeline = make_pipeline()
    pipeline.run()
