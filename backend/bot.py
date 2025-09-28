import pkg_resources
print(">>> Pipecat version:", pkg_resources.get_distribution("pipecat-ai").version)


import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Safe import for Pipecat WebRTC transport
from pipecat.transports.webrtc import WebRTCSFUTransport
transport = WebRTCSFUTransport()


from pipecat.pipeline import Pipeline
from pipecat.transports.services.openai import OpenAIChat
from pipecat.transports.services.deepgram import DeepgramSTT
from pipecat.transports.services.cartesia import CartesiaTTS

app = Flask(__name__)

@app.route("/call", methods=["POST"])
def call():
    """
    Start a minimal 3-turn prototype call.
    """

    # Setup services
    stt = DeepgramSTT(api_key=os.getenv("DEEPGRAM_API_KEY"))
    llm = OpenAIChat(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini")
    tts = CartesiaTTS(api_key=os.getenv("CARTESIA_API_KEY"))

    # WebRTC transport
    transport = WebRTCSFUTransport()

    # Pipeline
    pipeline = Pipeline([stt, llm, tts, transport])

    # Run conversation (dummy, 3 turns)
    conversation = [
        "Hello, who are you?",
        "Nice to meet you. Can you say something else?",
        "Great, this is the end of the test."
    ]

    responses = []
    for turn in conversation:
        response = pipeline.run(turn)
        responses.append(response)

    return jsonify({"status": "ok", "responses": responses})


@app.route("/")
def index():
    return "✅ Pipecat prototype backend is running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
