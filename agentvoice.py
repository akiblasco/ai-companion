import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai import conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from elevenlabs import play

load_dotenv()
#agent = ElevenLabs(agent_id=os.getenv("AGENT_ID"))
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))


audio = client.text_to_speech.convert(
    text="The quick brown fox jumps over the lazy dog.",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

play(audio)

'''
conversation = Conversation(
    # API client and agent ID.
    client,
    AGENT_ID,

    # Assume auth is required when API_KEY is set.
    requires_auth=bool(ELEVENLABS_API_KEY),

    # Use the default audio interface.
    audio_interface=DefaultAudioInterface(),

    # Simple callbacks that print the conversation to the console.
    callback_agent_response=lambda response: print(f"Agent: {response}"),
    callback_agent_response_correction=lambda original, corrected: print(f"Agent: {original} -> {corrected}"),
    callback_user_transcript=lambda transcript: print(f"User: {transcript}"),

    # Uncomment if you want to see latency measurements.
    # callback_latency_measurement=lambda latency: print(f"Latency: {latency}ms"),
)
'''

