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
    # Mateus — voz masculina clara em PT-BR (padrão para JARBAS)
    ELEVENLABS_VOICE_ID: str = os.getenv("ELEVENLABS_VOICE_ID", "XrExE9yKIg1WjnnlVkGX")

    # ── Tavily Web Search ──────────────────────────────────────────────────
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

    # ── YouTube Data API ───────────────────────────────────────────────────
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")
    # JSON array: [{"alias": "meu_canal", "channel_id": "UCxxxxxxx"}]
    YOUTUBE_CHANNELS: str = os.getenv("YOUTUBE_CHANNELS", "[]")

    # ── Facebook / Instagram ───────────────────────────────────────────────
    FACEBOOK_PAGE_TOKEN: str = os.getenv("FACEBOOK_PAGE_TOKEN", "")
    FACEBOOK_PAGE_ID: str = os.getenv("FACEBOOK_PAGE_ID", "1282247241627685")

    # ── Google Drive / Gmail ───────────────────────────────────────────────
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REFRESH_TOKEN: str = os.getenv("GOOGLE_REFRESH_TOKEN", "")

    # ── Security ───────────────────────────────────────────────────────────
    SECRET_KEY: str = os.getenv("SECRET_KEY", "jarbas-dev-secret-change-in-production")

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
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2048"))

    # How many past messages to include in context
    HISTORY_LIMIT: int = int(os.getenv("HISTORY_LIMIT", "20"))

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
            "youtube": bool(self.YOUTUBE_API_KEY),
            "version": self.APP_VERSION,
        }


# Singleton instance used throughout the app
config = Config()
