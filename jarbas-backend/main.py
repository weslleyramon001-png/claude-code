"""
JARBAS FastAPI Server — Main entry point.

Endpoints:
  POST /chat          — Send a message, get a response
  GET  /history       — Get conversation history for a session
  POST /clear         — Clear a session's history
  GET  /health        — Health check
  POST /voice         — Convert text to speech (ElevenLabs)
  WS   /ws/{session}  — WebSocket for streaming responses
  GET  /status        — Full service status dashboard
  GET  /export/{id}   — Export conversation history (JSON or TXT)

Run with:
  python main.py
  — or —
  uvicorn main:app --host 0.0.0.0 --port 8000 --reload
"""

import json
import asyncio
from typing import Optional

import anthropic
import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Security, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from config import config
from memory import (
    save_message,
    get_history,
    clear_session,
    get_facts_as_string,
    auto_extract_and_save,
    get_balance,
    list_movements,
    list_reminders,
    create_reminder,
    complete_reminder,
)
from personality import get_system_prompt
from tools import format_tools_for_claude, process_tool_call
from voice import text_to_speech


# ── Auth ───────────────────────────────────────────────────────────────────

_bearer = HTTPBearer(auto_error=False)


def require_auth(credentials: HTTPAuthorizationCredentials = Security(_bearer)):
    """Dependency: validates Bearer token if ACCESS_TOKEN is configured."""
    if not config.ACCESS_TOKEN:
        return  # open access when no token configured
    if not credentials or credentials.credentials != config.ACCESS_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido. Acesso negado.")


# ── App setup ──────────────────────────────────────────────────────────────

app = FastAPI(
    title="JARBAS API",
    description="Just A Rather Brilliant Autonomous System — Backend API",
    version=config.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos estáticos (produtos, páginas públicas)
_static_dir = Path(__file__).parent / "static"
if _static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(_static_dir)), name="static")


# ── Request / Response models ──────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    response: str
    session_id: str
    tool_calls_made: list[str] = []


class ClearRequest(BaseModel):
    session_id: str = "default"


class VoiceRequest(BaseModel):
    text: str
    voice_id: Optional[str] = None


class ReminderCreate(BaseModel):
    title: str
    description: str = ""
    due_date: str = ""


# ── Core chat logic (shared by /chat and WebSocket) ───────────────────────

async def run_agent(
    user_message: str,
    session_id: str,
    stream_callback=None,
    event_callback=None,
) -> tuple[str, list[str]]:
    """
    Core agentic loop:
      1. Save user message to memory
      2. Extract and persist facts from the message
      3. Build conversation context (history + system prompt with user facts)
      4. Call Claude with tools enabled
      5. Handle tool_use responses in a loop until Claude returns text
      6. Save assistant response to memory
      7. Return (full_response_text, list_of_tool_names_called)

    Args:
        user_message:    The raw user message string.
        session_id:      Conversation session identifier.
        stream_callback: Async callable(token: str) for streaming tokens to WebSocket.
                         Pass None for non-streaming (REST) mode.
        event_callback:  Async callable(event: dict) for sending special events (e.g. screenshots).

    Returns:
        Tuple of (assistant_response_text, tool_calls_made_list)
    """
    # ── 1. Persist user message & extract facts ────────────────────────────
    save_message(session_id, "user", user_message)
    auto_extract_and_save(user_message)

    # ── 2. Build messages list from history ────────────────────────────────
    history = get_history(session_id, limit=config.HISTORY_LIMIT)
    # get_history returns the message we just saved, so we use it as-is
    messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in history
        if msg["role"] in ("user", "assistant")
    ]

    # ── 3. Build system prompt with current user facts ────────────────────
    user_facts = get_facts_as_string()
    system_prompt = get_system_prompt(user_facts)

    # ── 4. Initialise Anthropic client & tools ────────────────────────────
    client = anthropic.AsyncAnthropic(api_key=config.ANTHROPIC_API_KEY)
    tools = format_tools_for_claude()
    tool_calls_made: list[str] = []

    full_response = ""

    # ── 5. Agentic loop (handles chained tool calls) ──────────────────────
    current_messages = messages.copy()

    for _iteration in range(10):  # Safety cap: max 10 tool-call rounds
        if stream_callback:
            # ── Streaming mode (WebSocket) ────────────────────────────────
            response_text = ""
            tool_use_blocks = []
            stop_reason = None

            async with client.messages.stream(
                model=config.CLAUDE_MODEL,
                max_tokens=config.MAX_TOKENS,
                system=system_prompt,
                messages=current_messages,
                tools=tools,
            ) as stream:
                async for event in stream:
                    # Text delta — stream to client
                    if hasattr(event, "type"):
                        if event.type == "content_block_delta":
                            if hasattr(event.delta, "text"):
                                chunk = event.delta.text
                                response_text += chunk
                                await stream_callback(chunk)

                # Get the final message for stop_reason and tool_use blocks
                final_msg = await stream.get_final_message()
                stop_reason = final_msg.stop_reason
                tool_use_blocks = [
                    b for b in final_msg.content if b.type == "tool_use"
                ]
                # Capture full content for message history
                assistant_content = final_msg.content

        else:
            # ── Non-streaming mode (REST /chat) ───────────────────────────
            response = await client.messages.create(
                model=config.CLAUDE_MODEL,
                max_tokens=config.MAX_TOKENS,
                system=system_prompt,
                messages=current_messages,
                tools=tools,
            )
            stop_reason = response.stop_reason
            tool_use_blocks = [b for b in response.content if b.type == "tool_use"]
            # Extract text from content blocks
            response_text = " ".join(
                b.text for b in response.content if hasattr(b, "text") and b.text
            ).strip()
            assistant_content = response.content

        # ── If Claude stopped normally, we're done ────────────────────────
        if stop_reason != "tool_use" or not tool_use_blocks:
            full_response = response_text
            break

        # ── Process tool calls ────────────────────────────────────────────
        # Add assistant's turn (with tool_use blocks) to message history
        current_messages.append({
            "role": "assistant",
            "content": [b.model_dump() if hasattr(b, "model_dump") else b for b in assistant_content],
        })

        # Execute each tool and collect results
        tool_results = []
        for tool_block in tool_use_blocks:
            tool_name = tool_block.name
            tool_input = tool_block.input
            tool_calls_made.append(tool_name)

            result = await process_tool_call(tool_name, tool_input, config)

            # Screenshot results: send image to UI + pass as vision to Claude
            if isinstance(result, dict) and "base64" in result:
                if event_callback:
                    await event_callback({
                        "type": "screenshot",
                        "url": result.get("url", ""),
                        "base64": result["base64"],
                    })
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_block.id,
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": result["base64"],
                            },
                        },
                        {
                            "type": "text",
                            "text": f"Screenshot de {result.get('url', 'URL')} capturado. Descreva o que você vê para o Ramon.",
                        },
                    ],
                })
            elif isinstance(result, dict) and "error" in result:
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_block.id,
                    "content": result["error"],
                })
            else:
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_block.id,
                    "content": result,
                })

        # Feed tool results back as a user turn
        current_messages.append({
            "role": "user",
            "content": tool_results,
        })

        # Continue loop — Claude will process tool results and respond
        continue

    # ── 6. Persist assistant response ─────────────────────────────────────
    if full_response:
        save_message(
            session_id,
            "assistant",
            full_response,
            metadata={"tools_used": tool_calls_made} if tool_calls_made else {},
        )

    return full_response, tool_calls_made


# ── REST Endpoints ─────────────────────────────────────────────────────────

@app.get("/arsenal-ia", response_class=HTMLResponse, include_in_schema=False)
async def arsenal_ia_page():
    """Página do produto ARSENAL IA — pública, sem autenticação."""
    html_path = _static_dir / "arsenal-ia.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))


@app.get("/arsenal-ia-vendas", response_class=HTMLResponse, include_in_schema=False)
async def arsenal_ia_vendas_page():
    """Página de vendas do ARSENAL IA — pública, sem autenticação."""
    html_path = _static_dir / "arsenal-ia-vendas.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))


@app.get("/ebook-primeiros-passos", response_class=HTMLResponse, include_in_schema=False)
async def ebook_primeiros_passos_page():
    """Ebook: Primeiros Passos no Digital — público."""
    html_path = _static_dir / "ebook-primeiros-passos.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))


@app.get("/clube-wl", response_class=HTMLResponse, include_in_schema=False)
async def clube_wl_page():
    """Clube WL-Solucion — página de vendas da comunidade VIP."""
    html_path = _static_dir / "clube-wl.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))


@app.get("/health")
async def health():
    """Quick health check — always returns 200 OK if the server is up."""
    return {
        "status": "ok",
        "version": config.APP_VERSION,
        "jarbas": "online",
        "services": config.status_report(),
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, _=Depends(require_auth)):
    """
    Send a message to JARBAS and get a response.

    Returns 503 if ANTHROPIC_API_KEY is not configured.
    """
    if not config.is_ready():
        raise HTTPException(
            status_code=503,
            detail={
                "error": "JARBAS não configurado",
                "message": (
                    "A chave ANTHROPIC_API_KEY não foi configurada. "
                    "Copie .env.example para .env e adicione sua chave da API Anthropic. "
                    "Obtenha sua chave em: https://console.anthropic.com/"
                ),
                "setup": "Veja o arquivo SETUP.md para instruções completas.",
            },
        )

    try:
        response_text, tool_calls = await run_agent(
            user_message=request.message,
            session_id=request.session_id,
        )
        return ChatResponse(
            response=response_text,
            session_id=request.session_id,
            tool_calls_made=tool_calls,
        )
    except anthropic.AuthenticationError:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "API key inválida",
                "message": "A chave ANTHROPIC_API_KEY está configurada mas é inválida. Verifique o valor no seu .env.",
            },
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={"error": "Erro interno", "message": str(exc)},
        )


@app.get("/history")
async def history(session_id: str = "default", _=Depends(require_auth)):
    """Return conversation history for a session."""
    msgs = get_history(session_id, limit=50)
    return {"session_id": session_id, "messages": msgs, "count": len(msgs)}


@app.post("/clear")
async def clear(request: ClearRequest, _=Depends(require_auth)):
    """Clear all messages for a session."""
    clear_session(request.session_id)
    return {"status": "ok", "session_id": request.session_id, "message": "Histórico apagado."}


@app.get("/status")
async def full_status():
    """Dashboard completo — verifica todos os serviços integrados."""
    services = {}

    # Anthropic
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get("https://api.anthropic.com")
        services["anthropic"] = "online" if r.status_code < 500 else "degraded"
    except Exception:
        services["anthropic"] = "offline"

    # ElevenLabs
    if config.ELEVENLABS_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.get(
                    "https://api.elevenlabs.io/v1/user",
                    headers={"xi-api-key": config.ELEVENLABS_API_KEY},
                )
            services["elevenlabs"] = "online" if r.status_code == 200 else "error"
        except Exception:
            services["elevenlabs"] = "offline"
    else:
        services["elevenlabs"] = "not configured"

    # Tavily
    services["tavily"] = "configured" if config.TAVILY_API_KEY else "not configured"

    # Database
    try:
        get_history("__healthcheck__")
        services["database"] = "online"
    except Exception:
        services["database"] = "offline"

    return {
        "status": "online",
        "version": config.APP_VERSION,
        "services": services,
    }


@app.get("/export/{session_id}")
async def export_history(session_id: str, format: str = "json"):
    """Exporta o histórico de conversa em JSON ou TXT."""
    msgs = get_history(session_id, limit=200)
    if format == "txt":
        lines = [f"[{m['role'].upper()}] {m['content']}" for m in msgs]
        content = "\n\n".join(lines)
        return Response(
            content=content,
            media_type="text/plain",
            headers={"Content-Disposition": f"attachment; filename=jarbas_{session_id}.txt"},
        )
    return JSONResponse({"session_id": session_id, "messages": msgs, "count": len(msgs)})


@app.post("/voice")
async def voice(request: VoiceRequest, _=Depends(require_auth)):
    """
    Convert text to speech via ElevenLabs and return audio/mpeg.

    Returns 503 if ELEVENLABS_API_KEY is not configured.
    """
    if not config.ELEVENLABS_API_KEY:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "Voz não configurada",
                "message": (
                    "A chave ELEVENLABS_API_KEY não foi configurada. "
                    "Obtenha sua chave gratuita em: https://elevenlabs.io/"
                ),
            },
        )

    voice_id = request.voice_id or config.ELEVENLABS_VOICE_ID
    audio_bytes = await text_to_speech(
        text=request.text,
        api_key=config.ELEVENLABS_API_KEY,
        voice_id=voice_id,
    )

    if audio_bytes is None:
        raise HTTPException(
            status_code=503,
            detail={"error": "Falha na síntese de voz", "message": "ElevenLabs retornou erro. Verifique a chave e tente novamente."},
        )

    return Response(content=audio_bytes, media_type="audio/mpeg")


# ── WebSocket ──────────────────────────────────────────────────────────────

@app.get("/finance/balance")
async def finance_balance(_=Depends(require_auth)):
    """Retorna saldo financeiro atual (entradas, saídas, líquido)."""
    return get_balance()


@app.get("/finance/movements")
async def finance_movements(limit: int = 20, category: str = "", _=Depends(require_auth)):
    """Retorna movimentos financeiros recentes."""
    mvs = list_movements(limit=limit, category=category if category else None)
    return {"movements": mvs, "count": len(mvs)}


@app.get("/reminders")
async def get_reminders(include_completed: bool = False, _=Depends(require_auth)):
    """Lista lembretes (pendentes por padrão)."""
    return {"reminders": list_reminders(include_completed), "count": len(list_reminders(include_completed))}


@app.post("/reminders")
async def post_reminder(body: ReminderCreate, _=Depends(require_auth)):
    """Cria um novo lembrete."""
    rid = create_reminder(body.title, body.description, body.due_date)
    return {"id": rid, "title": body.title, "description": body.description, "due_date": body.due_date}


@app.patch("/reminders/{reminder_id}/complete")
async def patch_reminder_complete(reminder_id: int, _=Depends(require_auth)):
    """Marca um lembrete como concluído."""
    success = complete_reminder(reminder_id)
    if not success:
        raise HTTPException(status_code=404, detail="Lembrete não encontrado ou já concluído.")
    return {"status": "ok", "reminder_id": reminder_id}


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str, token: str = ""):
    """
    WebSocket endpoint for real-time streaming.

    Client sends:  {"message": "texto do usuário"}
    Server emits:  {"type": "token",      "content": "..."}         — one per streamed token
                   {"type": "screenshot", "url": "...", "base64": "..."} — browser screenshot
                   {"type": "done",       "full_response": "...", "tool_calls": [...]}
                   {"type": "error",      "message": "..."}
    """
    if config.ACCESS_TOKEN and token != config.ACCESS_TOKEN:
        await websocket.close(code=4001, reason="Unauthorized")
        return
    await websocket.accept()

    try:
        while True:
            # Wait for client message
            raw = await websocket.receive_text()

            try:
                data = json.loads(raw)
                user_message = data.get("message", "").strip()
            except json.JSONDecodeError:
                await websocket.send_json({"type": "error", "message": "JSON inválido."})
                continue

            if not user_message:
                await websocket.send_json({"type": "error", "message": "Mensagem vazia."})
                continue

            if not config.is_ready():
                await websocket.send_json({
                    "type": "error",
                    "message": (
                        "JARBAS não configurado — ANTHROPIC_API_KEY ausente. "
                        "Veja SETUP.md para instruções."
                    ),
                })
                continue

            # Stream callback — sends each token as a JSON message
            async def stream_token(token: str):
                await websocket.send_json({"type": "token", "content": token})

            async def send_event(event: dict):
                await websocket.send_json(event)

            try:
                full_response, tool_calls = await run_agent(
                    user_message=user_message,
                    session_id=session_id,
                    stream_callback=stream_token,
                    event_callback=send_event,
                )
                await websocket.send_json({
                    "type": "done",
                    "full_response": full_response,
                    "tool_calls": tool_calls,
                })
            except anthropic.AuthenticationError:
                await websocket.send_json({
                    "type": "error",
                    "message": "API key Anthropic inválida. Verifique ANTHROPIC_API_KEY no .env.",
                })
            except Exception as exc:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Erro interno: {exc}",
                })

    except WebSocketDisconnect:
        # Client disconnected — clean exit, no error
        pass


# ── Entry point ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    print(f"\n{'='*50}")
    print(f"  JARBAS v{config.APP_VERSION} — Iniciando...")
    print(f"{'='*50}")
    print(f"  Claude:      {'OK' if config.ANTHROPIC_API_KEY else 'NÃO CONFIGURADO'}")
    print(f"  Voz:         {'OK' if config.ELEVENLABS_API_KEY else 'NÃO CONFIGURADO'}")
    print(f"  Web Search:  {'OK' if config.TAVILY_API_KEY else 'NÃO CONFIGURADO'}")
    print(f"  Porta:       {config.PORT}")
    print(f"{'='*50}\n")

    if not config.is_ready():
        print("  AVISO: ANTHROPIC_API_KEY não configurada.")
        print("  Copie .env.example -> .env e adicione sua chave.")
        print("  O servidor vai iniciar mas /chat retornará 503.\n")

    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=False,
        log_level="info",
    )
