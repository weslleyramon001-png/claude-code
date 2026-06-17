from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx, json, asyncio, uuid
from config import ANTHROPIC_KEY, AI_MODEL, AI_MAX_TOKENS, ELEVENLABS_KEY, ELEVENLABS_VOICE_ID
from memory import init_db, save_message, get_history, clear_session, get_long_term_context, save_fact
from personality import build_system_prompt

app = FastAPI(title="JARBAS API", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

init_db()

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class FactRequest(BaseModel):
    category: str
    key: str
    value: str

@app.get("/health")
async def health():
    return {"status": "online", "agent": "JARBAS", "version": "1.0.0"}

@app.post("/chat")
async def chat(req: ChatRequest):
    if not ANTHROPIC_KEY:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY não configurada")

    save_message(req.session_id, "user", req.message)
    history = get_history(req.session_id, limit=20)
    long_term = get_long_term_context()
    system = build_system_prompt(long_term)

    async with httpx.AsyncClient(timeout=60) as client:
        res = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": AI_MODEL,
                "max_tokens": AI_MAX_TOKENS,
                "system": system,
                "messages": history
            }
        )
        if res.status_code != 200:
            raise HTTPException(status_code=res.status_code, detail=res.text)
        data = res.json()
        reply = data["content"][0]["text"]

    save_message(req.session_id, "assistant", reply)
    return {"reply": reply, "session_id": req.session_id}

@app.websocket("/ws/{session_id}")
async def websocket_chat(ws: WebSocket, session_id: str):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_text()
            payload = json.loads(data)
            message = payload.get("message", "")
            if not message: continue

            save_message(session_id, "user", message)
            history = get_history(session_id, limit=20)
            system = build_system_prompt(get_long_term_context())

            async with httpx.AsyncClient(timeout=60) as client:
                async with client.stream(
                    "POST",
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": ANTHROPIC_KEY,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json"
                    },
                    json={
                        "model": AI_MODEL,
                        "max_tokens": AI_MAX_TOKENS,
                        "system": system,
                        "messages": history,
                        "stream": True
                    }
                ) as response:
                    full_reply = ""
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            chunk = line[6:]
                            if chunk == "[DONE]": break
                            try:
                                obj = json.loads(chunk)
                                if obj.get("type") == "content_block_delta":
                                    text = obj["delta"].get("text", "")
                                    full_reply += text
                                    await ws.send_text(json.dumps({"type": "chunk", "text": text}))
                            except: pass
                    save_message(session_id, "assistant", full_reply)
                    await ws.send_text(json.dumps({"type": "done", "full": full_reply}))

    except WebSocketDisconnect:
        pass

@app.get("/history/{session_id}")
async def history(session_id: str):
    return {"history": get_history(session_id)}

@app.post("/clear/{session_id}")
async def clear(session_id: str):
    clear_session(session_id)
    return {"status": "cleared"}

@app.post("/fact")
async def add_fact(req: FactRequest):
    save_fact(req.category, req.key, req.value)
    return {"status": "saved"}

@app.get("/voice/{text}")
async def voice(text: str):
    if not ELEVENLABS_KEY:
        raise HTTPException(status_code=500, detail="ELEVENLABS_API_KEY não configurada")
    async with httpx.AsyncClient(timeout=30) as client:
        res = await client.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}",
            headers={"xi-api-key": ELEVENLABS_KEY, "content-type": "application/json"},
            json={"text": text[:500], "model_id": "eleven_multilingual_v2",
                  "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}}
        )
        if res.status_code != 200:
            raise HTTPException(status_code=res.status_code, detail="Erro ElevenLabs")
        return StreamingResponse(asyncio.to_thread(lambda: res.content),
                                 media_type="audio/mpeg")
