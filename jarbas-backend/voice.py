"""
JARBAS Voice Module — ElevenLabs text-to-speech integration.

Uses the ElevenLabs v1 API to convert text to speech.
Tuned for a clear, authoritative JARVIS-style delivery.

Returns audio bytes (audio/mpeg) on success, None on failure.
"""

import httpx
from typing import Optional


# ── TTS settings ───────────────────────────────────────────────────────────

# Tuned for JARVIS-style: consistent, measured, authoritative
_VOICE_SETTINGS = {
    "stability": 0.75,          # Higher = more consistent, less erratic
    "similarity_boost": 0.85,   # Stay close to Daniel's original voice
    "style": 0.15,              # Low style = formal, not theatrical
    "use_speaker_boost": True,  # Boost voice clarity
}

_ELEVENLABS_BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech"
_TIMEOUT_SECONDS = 30.0


# ── Main function ──────────────────────────────────────────────────────────

async def text_to_speech(
    text: str,
    api_key: str,
    voice_id: str,
) -> Optional[bytes]:
    """
    Convert text to speech via the ElevenLabs v1 API.

    Args:
        text:     The text to convert. Keep under 5000 characters for best results.
        api_key:  ElevenLabs API key (ELEVENLABS_API_KEY).
        voice_id: ElevenLabs voice ID (ELEVENLABS_VOICE_ID).
                  Default is "onwK4e9ZLuTAKqWW03F9" (Daniel — British male).

    Returns:
        Raw audio bytes (audio/mpeg) on success.
        None if no API key is configured or if an error occurs.
    """
    if not api_key:
        return None

    if not text or not text.strip():
        return None

    text_clean = text.strip()
    if len(text_clean) > 4500:
        text_clean = text_clean[:4500] + "..."

    url = f"{_ELEVENLABS_BASE_URL}/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": text_clean,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": _VOICE_SETTINGS,
    }

    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT_SECONDS) as client:
            response = await client.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                return response.content

            if response.status_code == 401:
                print("[JARBAS Voice] ElevenLabs API key inválida (401 Unauthorized).")
                return None

            if response.status_code == 422:
                print(f"[JARBAS Voice] Parâmetros inválidos (422): {response.text[:200]}")
                return None

            if response.status_code == 429:
                print("[JARBAS Voice] Limite de requisições ElevenLabs atingido (429).")
                return None

            print(f"[JARBAS Voice] Erro inesperado HTTP {response.status_code}: {response.text[:200]}")
            return None

    except httpx.TimeoutException:
        print(f"[JARBAS Voice] Timeout ao conectar com ElevenLabs ({_TIMEOUT_SECONDS}s).")
        return None
    except httpx.ConnectError:
        print("[JARBAS Voice] Falha de conexão com ElevenLabs. Verifique sua internet.")
        return None
    except Exception as exc:
        print(f"[JARBAS Voice] Erro inesperado: {exc}")
        return None
