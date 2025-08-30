import os
from dotenv import load_dotenv

# Load environment variables from voice.env file
load_dotenv("voice.env")

AGENT_ID = os.getenv("AGENT_ID")
API_KEY = os.getenv("API_KEY")

# Debug: Print loaded values
print(f"Loaded API_KEY: {API_KEY}")
print(f"Loaded AGENT_ID: {AGENT_ID}")

# Validate that values are loaded
if not API_KEY:
    raise ValueError("API_KEY tidak ditemukan. Pastikan file voice.env berisi API_KEY yang valid.")

if not AGENT_ID:
    raise ValueError("AGENT_ID tidak ditemukan. Pastikan file voice.env berisi AGENT_ID yang valid.")

from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from elevenlabs.types import ConversationConfig

# Define callback functions first
def print_agent_response(response):
    print(f"Agent: {response}")

def print_interrupted_response(original, corrected):
    print(f"Agent interrupted, truncated response: {corrected}")

def print_user_transcript(transcript):
    print(f"User: {transcript}")
    
    # Check for shutdown commands
    shutdown_commands = ["shutdown", "exit", "quit", "stop", "close", "terminate", "bye", "goodbye"]
    if any(command in transcript.lower() for command in shutdown_commands):
        print("Shutdown command detected. Stopping voice assistant...")
        global conversation
        try:
            conversation.end_session()
        except:
            pass
        exit(0)

user_name = "Afika"
schedule = "Sales Meeting with Taipy at 10:00; Gym with Sophie at 17:00"
prompt = f"""You are a friendly, conversational AI assistant and companion to {user_name}. You can discuss anything - from casual conversations, fun facts, jokes, personal advice, to helping with daily tasks. 

You have access to {user_name}'s schedule: {schedule}. You can help with schedule-related questions when asked, but you're not limited to just that. 

Feel free to:
- Chat about any topic naturally
- Share interesting fun facts when asked
- Give advice and listen when they want to talk/vent
- Tell jokes or be entertaining
- Discuss hobbies, movies, books, or anything else
- Be supportive and empathetic

Be conversational, warm, and engaging like a good friend. If the user asks how to stop or shutdown the assistant, tell them they can say 'shutdown', 'exit', 'quit', 'stop', 'close', 'terminate', 'bye', or 'goodbye'."""

first_message = f"Hello {user_name}! I'm your AI companion. I can help with your schedule, chat about anything, share fun facts, or just be here if you want to talk. What's on your mind today?"

conversation_override = {
    "agent": {
        "prompt": {
            "prompt": prompt,
        },
        "first_message": first_message,
    },
}

config = ConversationConfig(
    conversation_config_override=conversation_override,
    extra_body={},
    dynamic_variables={},
    user_id="user_dicky_123",
)

client = ElevenLabs(api_key=API_KEY)

# Create conversation with all callbacks
conversation = Conversation(
    client,
    AGENT_ID,
    config=config,
    requires_auth=True,
    audio_interface=DefaultAudioInterface(),
    callback_agent_response=print_agent_response,
    callback_agent_response_correction=print_interrupted_response,
    callback_user_transcript=print_user_transcript,
)

try:
    conversation.start_session()
except Exception as e:
    print(f"Error occurred: {e}")
    print("Check your microphone settings or API permissions.")