"""
JARBAS Configuration Module
Loads all API keys and settings from environment variables via python-dotenv.
"""

import os
from dotenv import load_dotenv

# Load .env file if it exists (development mode)
load_dotenv()


class Config:
    """Central configuration class — all settings in one place."""

    # ── Anthropic / Claude ─────────────────────────────────────────────────
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    # ── ElevenLabs Voice ───────────────────────────────────────────────────
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    # Daniel — voz britânica masculina, autoritária, estilo JARVIS
    ELEVENLABS_VOICE_ID: str = os.getenv("ELEVENLABS_VOICE_ID", "onwK4e9ZLuTAKqWW03F9")

    # ── Tavily Web Search ──────────────────────────────────────────────────
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

    # ── Security ───────────────────────────────────────────────────────────
    SECRET_KEY: str = os.getenv("SECRET_KEY", "jarbas-dev-secret-change-in-production")
    # Token de acesso para proteger a API. Deixe vazio para acesso aberto (dev local).
    ACCESS_TOKEN: str = os.getenv("ACCESS_TOKEN", "")

    # ── CORS ───────────────────────────────────────────────────────────────
    # Comma-separated list of allowed origins, e.g. "https://myapp.com,https://jarbas.up.railway.app"
    ALLOWED_ORIGINS_RAW: str = os.getenv("ALLOWED_ORIGINS", "*")

    # ── Database ───────────────────────────────────────────────────────────
    DB_PATH: str = os.getenv("DB_PATH", "jarbas_memory.db")

    # ── App settings ───────────────────────────────────────────────────────
    APP_VERSION: str = "1.0.0"
    APP_NAME: str = "JARBAS"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Claude model
    CLAUDE_MODEL: str = "claude-sonnet-4-6"

    # Max tokens for Claude responses
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "4096"))

    # How many past messages to include in context
    HISTORY_LIMIT: int = int(os.getenv("HISTORY_LIMIT", "30"))

    @property
    def allowed_origins(self) -> list[str]:
        """Parse ALLOWED_ORIGINS into a list. '*' becomes ['*']."""
        if self.ALLOWED_ORIGINS_RAW.strip() == "*":
            return ["*"]
        return [o.strip() for o in self.ALLOWED_ORIGINS_RAW.split(",") if o.strip()]

    def is_ready(self) -> bool:
        """Return True if the minimum required key (Anthropic) is configured."""
        return bool(self.ANTHROPIC_API_KEY)

    def status_report(self) -> dict:
        """Return a dict showing which services are configured (without exposing keys)."""
        return {
            "claude": bool(self.ANTHROPIC_API_KEY),
            "voice": bool(self.ELEVENLABS_API_KEY),
            "web_search": bool(self.TAVILY_API_KEY),
            "version": self.APP_VERSION,
        }


# Singleton instance used throughout the app
config = Config()
