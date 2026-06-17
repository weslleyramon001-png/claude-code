import os
from dotenv import load_dotenv
load_dotenv()

ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")  # Adam (pt-BR friendly)
AI_MODEL = "claude-sonnet-4-6"
AI_MAX_TOKENS = 1024
MEMORY_DB = "jarbas_memory.db"
SECRET_KEY = os.getenv("SECRET_KEY", "jarbas-secret-2026")
AGENT_NAME = os.getenv("AGENT_NAME", "JARBAS")
OWNER_NAME = os.getenv("OWNER_NAME", "Weslley")
