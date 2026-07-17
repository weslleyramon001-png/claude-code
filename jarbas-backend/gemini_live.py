"""
Gemini Live — ponte bidirecional entre o frontend do JARBAS e a Gemini Live API.

Fluxo:
  Browser → WebSocket /ws/gemini/{session} → JARBAS Backend → Gemini Live API (WebSocket)

O browser captura áudio PCM 16kHz/16-bit/mono, envia em chunks base64.
O Gemini responde com texto e/ou áudio (PCM 24kHz).
"""

import asyncio
import json
import logging
import os

import websockets

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_LIVE_URL = (
    "wss://generativelanguage.googleapis.com/ws/"
    "google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent"
)
GEMINI_MODEL = "models/gemini-2.0-flash-exp"

SYSTEM_PROMPT = (
    "Você é o JARBAS, assistente de IA pessoal do Ramon (Weslley Ramon). "
    "Responda sempre em português brasileiro, de forma direta, objetiva e útil. "
    "Seja como o JARVIS do Homem de Ferro: eficiente, inteligente e confiante."
)


async def run_gemini_live_session(client_ws, session_id: str):
    """
    Gerencia uma sessão completa com o Gemini Live API.
    Faz ponte bidirecional entre o WebSocket do cliente e o Gemini.

    Mensagens recebidas do cliente:
      {"type": "audio_chunk", "data": "<base64 PCM 16kHz>"}
      {"type": "text", "message": "texto do usuário"}
      {"type": "end_turn"}

    Mensagens enviadas ao cliente:
      {"type": "gemini_ready"}
      {"type": "gemini_text", "content": "texto da resposta"}
      {"type": "gemini_audio", "data": "<base64 PCM 24kHz>", "mime_type": "audio/pcm;rate=24000"}
      {"type": "gemini_turn_complete"}
      {"type": "error", "message": "..."}
    """
    if not GEMINI_API_KEY:
        await client_ws.send_json({
            "type": "error",
            "message": "GEMINI_API_KEY não configurada. Adicione no Railway."
        })
        return

    url = f"{GEMINI_LIVE_URL}?key={GEMINI_API_KEY}"

    logger.info(f"[GeminiLive] Iniciando sessão {session_id}")
    try:
        async with websockets.connect(
            url,
            ping_interval=20,
            ping_timeout=30,
            close_timeout=10,
        ) as gemini_ws:
            logger.info("[GeminiLive] Conexão WebSocket aberta com o Gemini")

            # ── Configuração inicial da sessão ────────────────────────────
            setup = {
                "setup": {
                    "model": GEMINI_MODEL,
                    "generation_config": {
                        "response_modalities": ["AUDIO", "TEXT"],
                        "speech_config": {
                            "voice_config": {
                                "prebuilt_voice_config": {
                                    "voice_name": "Puck"
                                }
                            }
                        }
                    },
                    "system_instruction": {
                        "parts": [{"text": SYSTEM_PROMPT}]
                    }
                }
            }
            await gemini_ws.send(json.dumps(setup))

            # Aguarda confirmação do setup
            raw = await asyncio.wait_for(gemini_ws.recv(), timeout=10.0)
            data = json.loads(raw)
            logger.info(f"[GeminiLive] Resposta do setup: {data}")
            if "setupComplete" not in data:
                msg = f"Gemini não confirmou setup: {data}"
                logger.error(f"[GeminiLive] {msg}")
                await client_ws.send_json({"type": "error", "message": msg})
                return

            await client_ws.send_json({"type": "gemini_ready"})

            # ── Tarefa 1: cliente → Gemini ────────────────────────────────
            async def client_to_gemini():
                try:
                    while True:
                        raw_client = await client_ws.receive_text()
                        msg = json.loads(raw_client)
                        mtype = msg.get("type", "")

                        if mtype == "audio_chunk":
                            payload = {
                                "realtime_input": {
                                    "media_chunks": [{
                                        "mime_type": "audio/pcm;rate=16000",
                                        "data": msg["data"]
                                    }]
                                }
                            }
                            await gemini_ws.send(json.dumps(payload))

                        elif mtype == "text":
                            payload = {
                                "client_content": {
                                    "turns": [{
                                        "role": "user",
                                        "parts": [{"text": msg.get("message", "")}]
                                    }],
                                    "turn_complete": True
                                }
                            }
                            await gemini_ws.send(json.dumps(payload))

                        elif mtype == "end_turn":
                            payload = {
                                "client_content": {"turn_complete": True}
                            }
                            await gemini_ws.send(json.dumps(payload))

                except Exception:
                    pass

            # ── Tarefa 2: Gemini → cliente ────────────────────────────────
            async def gemini_to_client():
                try:
                    async for raw_gemini in gemini_ws:
                        data = json.loads(raw_gemini)

                        server_content = data.get("serverContent", {})
                        model_turn = server_content.get("modelTurn", {})
                        parts = model_turn.get("parts", [])

                        for part in parts:
                            if "text" in part and part["text"]:
                                await client_ws.send_json({
                                    "type": "gemini_text",
                                    "content": part["text"]
                                })
                            elif "inlineData" in part:
                                await client_ws.send_json({
                                    "type": "gemini_audio",
                                    "data": part["inlineData"]["data"],
                                    "mime_type": part["inlineData"].get(
                                        "mimeType", "audio/pcm;rate=24000"
                                    )
                                })

                        if server_content.get("turnComplete"):
                            await client_ws.send_json({"type": "gemini_turn_complete"})

                except Exception:
                    pass

            # Rodar as duas direções em paralelo
            await asyncio.gather(
                client_to_gemini(),
                gemini_to_client(),
                return_exceptions=True
            )

    except websockets.exceptions.InvalidURI as exc:
        logger.error(f"[GeminiLive] URL inválida: {exc}")
        await client_ws.send_json({"type": "error", "message": "URL do Gemini Live inválida."})
    except websockets.exceptions.InvalidStatusCode as exc:
        logger.error(f"[GeminiLive] Status inválido {exc.status_code}: {exc.headers}")
        await client_ws.send_json({"type": "error", "message": f"Gemini recusou conexão: HTTP {exc.status_code}"})
    except Exception as exc:
        logger.error(f"[GeminiLive] Erro inesperado: {type(exc).__name__}: {exc}")
        await client_ws.send_json({"type": "error", "message": f"Erro Gemini Live: {type(exc).__name__}: {exc}"})
