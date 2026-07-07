"""
JARBAS Agent Tools

All tools are async functions that Claude can invoke via tool_use.
Each tool has a corresponding entry in the Claude tools list format.
"""

import math
import os
import re
import subprocess
import platform
from datetime import datetime
from typing import Any
import httpx
import pytz
import psutil
from browser import take_screenshot, browse_and_read
from config import config


# ── Tool implementations ─────────────────────────────────────────────────

async def get_current_datetime() -> str:
    tz = pytz.timezone("America/Sao_Paulo")
    now = datetime.now(tz)
    weekdays = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
    months = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ]
    return (
        f"{weekdays[now.weekday()]}, {now.day} de {months[now.month - 1]} de {now.year} — "
        f"{now.strftime('%H:%M')} (horário de Brasília)"
    )


async def calculate(expression: str) -> str:
    safe_pattern = re.compile(r'^[\d\s\+\-\*/\(\)\.\,\%\*\^a-z_]+$', re.IGNORECASE)
    if not safe_pattern.match(expression):
        return "Expressão inválida. Apenas operações matemáticas são permitidas."

    safe_names: dict[str, Any] = {
        "sqrt": math.sqrt, "abs": abs, "round": round,
        "floor": math.floor, "ceil": math.ceil,
        "log": math.log, "log10": math.log10, "log2": math.log2,
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "pi": math.pi, "e": math.e, "pow": pow, "max": max, "min": min,
    }
    try:
        expr_clean = expression.replace("^", "**").replace(",", ".")
        result = eval(expr_clean, {"__builtins__": {}}, safe_names)  # noqa: S307
        if isinstance(result, float):
            if result == int(result):
                return str(int(result))
            return f"{result:,.6f}".rstrip("0").rstrip(".")
        return str(result)
    except ZeroDivisionError:
        return "Erro: divisão por zero."
    except Exception as exc:
        return f"Erro ao calcular: {exc}"


async def web_search(query: str, api_key: str) -> str:
    if not api_key:
        return (
            "Busca na web indisponível — chave da API Tavily não configurada. "
            "Adicione TAVILY_API_KEY no arquivo .env para habilitar esta função."
        )
    payload = {
        "api_key": api_key, "query": query, "search_depth": "basic",
        "include_answer": True, "include_raw_content": False, "max_results": 5,
    }
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post("https://api.tavily.com/search", json=payload)
            response.raise_for_status()
            data = response.json()
    except httpx.TimeoutException:
        return "Busca expirou. Tente novamente em instantes."
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 401:
            return "Chave da API Tavily inválida. Verifique o valor de TAVILY_API_KEY."
        return f"Erro na busca (HTTP {exc.response.status_code}). Tente novamente."
    except Exception as exc:
        return f"Erro inesperado na busca: {exc}"

    lines: list[str] = []
    answer = data.get("answer", "").strip()
    if answer:
        lines.append(f"**Resposta direta:** {answer}\n")
    results = data.get("results", [])
    if not results:
        return "Nenhum resultado encontrado para essa busca."
    lines.append("**Fontes:**")
    for i, r in enumerate(results[:5], 1):
        title = r.get("title", "Sem título")
        url = r.get("url", "")
        snippet = r.get("content", "")[:300].strip()
        lines.append(f"{i}. **{title}**")
        if snippet:
            lines.append(f"   {snippet}")
        if url:
            lines.append(f"   {url}")
        lines.append("")
    return "\n".join(lines).strip()


async def create_file_content(filename: str, content: str, file_type: str = "text") -> str:
    lang = file_type.lower().strip()
    return (
        f"**Arquivo: `{filename}`**\n\n"
        f"```{lang}\n{content}\n```\n\n"
        f"*Copie o conteúdo acima ou salve como `{filename}`.*"
    )


async def generate_pony_digital_content(content_type: str, topic: str) -> str:
    templates = {
        "hook": [
            f"Se você ainda não controla seu {topic}, você está deixando dinheiro na mesa.",
            f"Eu perdi R$3.000 por não usar {topic} certo. Hoje eu te mostro como evitar isso.",
            f"O segredo dos empreendedores que faturam mais está no {topic}. Veja o que ninguém te conta.",
            f"Para de fazer {topic} na mão. Existe uma forma mais inteligente — e gratuita.",
            f"Em 2 minutos você vai entender por que seu {topic} não está funcionando.",
        ],
        "caption": (
            f"A maioria das pessoas ignora {topic} até ser tarde demais.\n\n"
            f"Eu aprendi da forma difícil que controlar {topic} é o primeiro passo para qualquer negócio sério.\n\n"
            f"Por isso criei uma planilha que resolve isso de uma vez por todas.\n\n"
            f"👇 Link na bio para baixar agora.\n\n"
            f"#PonyDigital #Empreendedorismo #Planilhas #{topic.replace(' ', '')}"
        ),
        "email": (
            f"Assunto: Sobre o seu {topic}...\n\n"
            f"Olá,\n\nQuero falar sobre {topic} de uma forma diferente hoje.\n\n"
            f"A maioria das pessoas só pensa nisso quando o problema já explodiu.\n\n"
            f"Mas os empreendedores que realmente crescem tratam {topic} como prioridade desde o dia 1.\n\n"
            f"É por isso que criei a planilha de {topic} — para você ter controle total, sem complicação.\n\n"
            f"Clique aqui para ver: [LINK]\n\nAté mais,\nRamon"
        ),
        "cta": [
            f"👉 Baixe a planilha de {topic} — link na bio",
            f"✅ Acesse agora: planilha de {topic} com tudo pronto",
            f"🔗 Link na bio → Planilha de {topic} (oferta por tempo limitado)",
            f"💡 Quer dominar {topic}? Clica no link da bio",
        ],
        "headline": [
            f"Planilha de {topic.title()}: Controle Total em Menos de 5 Minutos",
            f"Chega de Perder Dinheiro com {topic.title()} — Use a Planilha Certa",
            f"O Sistema Definitivo de {topic.title()} para Empreendedores",
            f"Domine seu {topic.title()} com Esta Planilha Profissional",
        ],
    }
    ct = content_type.lower().strip()
    if ct not in templates:
        return f"Tipo '{content_type}' não reconhecido. Use: hook, caption, email, cta, ou headline."
    result = templates[ct]
    if isinstance(result, list):
        import random
        return f"**{content_type.upper()} para '{topic}':**\n\n" + "\n\n—\n\n".join(result)
    return f"**{content_type.upper()} para '{topic}':**\n\n{result}"


async def system_info() -> str:
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    boot = datetime.fromtimestamp(psutil.boot_time()).strftime("%d/%m/%Y %H:%M")
    lines = [
        f"🖥️ **Sistema: {platform.system()} {platform.release()}**",
        f"⚙️ CPU: **{cpu}%** em uso",
        f"🧠 RAM: **{ram.percent}%** em uso ({round(ram.used / 1e9, 1)} GB / {round(ram.total / 1e9, 1)} GB)",
        f"💾 Disco: **{disk.percent}%** em uso ({round(disk.used / 1e9, 1)} GB / {round(disk.total / 1e9, 1)} GB)",
        f"⏱️ Ligado desde: {boot}",
    ]
    return "\n".join(lines)


async def run_command(command: str, timeout: int = 30) -> str:
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=timeout
        )
        output = (result.stdout or result.stderr or "").strip()
        return output or "Comando executado sem output."
    except subprocess.TimeoutExpired:
        return f"Timeout após {timeout}s."
    except Exception as exc:
        return f"Erro: {exc}"


async def list_files(path: str) -> str:
    try:
        entries = os.listdir(path)
        if not entries:
            return f"Pasta `{path}` está vazia."
        lines = [f"📁 **{path}** ({len(entries)} itens)\n"]
        for e in sorted(entries):
            full = os.path.join(path, e)
            icon = "📁" if os.path.isdir(full) else "📄"
            lines.append(f"{icon} {e}")
        return "\n".join(lines)
    except FileNotFoundError:
        return f"Pasta não encontrada: `{path}`"
    except PermissionError:
        return f"Sem permissão para acessar: `{path}`"


async def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"📄 **{path}**\n\n```\n{content}\n```"
    except FileNotFoundError:
        return f"Arquivo não encontrado: `{path}`"
    except PermissionError:
        return f"Sem permissão para ler: `{path}`"
    except Exception as exc:
        return f"Erro ao ler arquivo: {exc}"


async def write_file(path: str, content: str) -> str:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ Arquivo salvo em `{path}`"
    except PermissionError:
        return f"Sem permissão para escrever em: `{path}`"
    except Exception as exc:
        return f"Erro ao salvar arquivo: {exc}"


async def youtube_search(query: str, api_key: str, max_results: int = 5) -> str:
    if not api_key:
        return "YouTube indisponível — adicione YOUTUBE_API_KEY no Railway."
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                "https://www.googleapis.com/youtube/v3/search",
                params={
                    "part": "snippet",
                    "q": query,
                    "type": "video",
                    "maxResults": max_results,
                    "relevanceLanguage": "pt",
                    "key": api_key,
                },
            )
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 403:
            return "Chave da YouTube API inválida ou cota esgotada."
        return f"Erro na YouTube API (HTTP {exc.response.status_code})."
    except Exception as exc:
        return f"Erro ao buscar no YouTube: {exc}"

    items = data.get("items", [])
    if not items:
        return f"Nenhum vídeo encontrado para '{query}'."

    lines = [f"**Resultados do YouTube para '{query}':**\n"]
    for i, item in enumerate(items, 1):
        snippet = item.get("snippet", {})
        video_id = item.get("id", {}).get("videoId", "")
        title = snippet.get("title", "Sem título")
        channel = snippet.get("channelTitle", "")
        description = snippet.get("description", "")[:150].strip()
        url = f"https://www.youtube.com/watch?v={video_id}"
        lines.append(f"{i}. **{title}**")
        lines.append(f"   Canal: {channel}")
        if description:
            lines.append(f"   {description}...")
        lines.append(f"   {url}\n")
    return "\n".join(lines).strip()


async def youtube_channel_stats(channel_id: str, api_key: str) -> str:
    if not api_key:
        return "YouTube indisponível — adicione YOUTUBE_API_KEY no Railway."
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                "https://www.googleapis.com/youtube/v3/channels",
                params={
                    "part": "snippet,statistics",
                    "id": channel_id,
                    "key": api_key,
                },
            )
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        return f"Erro ao buscar canal: {exc}"

    items = data.get("items", [])
    if not items:
        return f"Canal '{channel_id}' não encontrado."

    ch = items[0]
    snippet = ch.get("snippet", {})
    stats = ch.get("statistics", {})
    name = snippet.get("title", "?")
    description = snippet.get("description", "")[:200].strip()
    subscribers = int(stats.get("subscriberCount", 0))
    views = int(stats.get("viewCount", 0))
    videos = int(stats.get("videoCount", 0))

    lines = [
        f"**Canal: {name}**",
        f"👥 Inscritos: {subscribers:,}".replace(",", "."),
        f"▶️ Visualizações totais: {views:,}".replace(",", "."),
        f"🎬 Vídeos publicados: {videos}",
    ]
    if description:
        lines.append(f"\n📝 {description}")
    return "\n".join(lines)


async def get_weather(city: str) -> str:
    WMO_CODES = {
        0: "Céu limpo ☀️",
        1: "Principalmente limpo 🌤️", 2: "Parcialmente nublado ⛅", 3: "Nublado ☁️",
        45: "Névoa 🌫️", 48: "Névoa com gelo 🌫️",
        51: "Garoa leve 🌦️", 53: "Garoa moderada 🌦️", 55: "Garoa densa 🌧️",
        61: "Chuva fraca 🌧️", 63: "Chuva moderada 🌧️", 65: "Chuva forte 🌧️",
        71: "Neve fraca ❄️", 73: "Neve moderada ❄️", 75: "Neve forte ❄️",
        80: "Pancadas leves 🌦️", 81: "Pancadas moderadas ⛈️", 82: "Pancadas fortes ⛈️",
        95: "Tempestade ⚡", 96: "Tempestade com granizo ⚡", 99: "Tempestade forte com granizo ⚡",
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            geo_resp = await client.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": city, "count": 1, "language": "pt", "format": "json"},
            )
            geo_resp.raise_for_status()
            geo_data = geo_resp.json()

            results = geo_data.get("results", [])
            if not results:
                return f"Cidade '{city}' não encontrada. Verifique o nome e tente novamente."

            loc = results[0]
            lat, lon = loc["latitude"], loc["longitude"]
            city_name = loc.get("name", city)
            country = loc.get("country", "")

            wx_resp = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current_weather": True,
                    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode",
                    "timezone": "America/Sao_Paulo",
                    "forecast_days": 1,
                },
            )
            wx_resp.raise_for_status()
            wx = wx_resp.json()

        current = wx.get("current_weather", {})
        daily = wx.get("daily", {})

        temp_c = current.get("temperature", "?")
        wind_kmh = round(current.get("windspeed", 0))
        wmo = current.get("weathercode", 0)
        condition = WMO_CODES.get(wmo, f"Código {wmo}")

        tmax = daily.get("temperature_2m_max", [None])[0]
        tmin = daily.get("temperature_2m_min", [None])[0]
        precip = daily.get("precipitation_sum", [0])[0] or 0

        lines = [
            f"📍 **{city_name}, {country}**",
            f"🌡️ Temperatura atual: **{temp_c}°C** (máx {tmax}°C / mín {tmin}°C)",
            f"🌤️ Condição: {condition}",
            f"💧 Precipitação: {precip} mm",
            f"💨 Vento: {wind_kmh} km/h",
            f"\n*Fonte: Open-Meteo (dados em tempo real)*",
        ]
        return "\n".join(lines)

    except httpx.TimeoutException:
        return f"Timeout ao buscar clima para {city}. Tente novamente."
    except Exception as exc:
        return f"Erro ao buscar clima: {exc}"


# ── Facebook / Instagram ──────────────────────────────────────────────────

async def facebook_instagram_stats(token: str, page_id: str) -> str:
    if not token:
        return "Facebook/Instagram indisponível — adicione FACEBOOK_PAGE_TOKEN no Railway."
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            fb_resp = await client.get(
                f"https://graph.facebook.com/v19.0/{page_id}",
                params={
                    "fields": "name,fan_count,followers_count,instagram_business_account",
                    "access_token": token,
                },
            )
            fb_resp.raise_for_status()
            fb_data = fb_resp.json()

            lines = ["📊 **Suas redes sociais:**\n"]
            fb_name = fb_data.get("name", "Página")
            fb_fans = fb_data.get("fan_count", 0)
            fb_followers = fb_data.get("followers_count", 0)
            lines.append(f"**Facebook — {fb_name}**")
            lines.append(f"👍 Curtidas: {fb_fans:,}".replace(",", "."))
            lines.append(f"👥 Seguidores: {fb_followers:,}".replace(",", "."))

            ig_account = fb_data.get("instagram_business_account", {})
            if ig_account:
                ig_id = ig_account.get("id")
                ig_resp = await client.get(
                    f"https://graph.facebook.com/v19.0/{ig_id}",
                    params={
                        "fields": "username,followers_count,media_count",
                        "access_token": token,
                    },
                )
                ig_resp.raise_for_status()
                ig_data = ig_resp.json()
                ig_username = ig_data.get("username", "")
                ig_followers = ig_data.get("followers_count", 0)
                ig_media = ig_data.get("media_count", 0)
                lines.append(f"\n**Instagram — @{ig_username}**")
                lines.append(f"👥 Seguidores: {ig_followers:,}".replace(",", "."))
                lines.append(f"📸 Posts: {ig_media}")
            else:
                lines.append("\n_Instagram não vinculado à página._")

            return "\n".join(lines)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 401:
            return "Token do Facebook expirado ou inválido. Precisa renovar."
        return f"Erro na API do Facebook (HTTP {exc.response.status_code})."
    except Exception as exc:
        return f"Erro ao buscar dados do Facebook/Instagram: {exc}"


# ── Google OAuth helper ───────────────────────────────────────────────────

async def _google_access_token() -> str:
    """Troca o refresh_token por um access_token fresco."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": config.GOOGLE_CLIENT_ID,
                "client_secret": config.GOOGLE_CLIENT_SECRET,
                "refresh_token": config.GOOGLE_REFRESH_TOKEN,
                "grant_type": "refresh_token",
            },
        )
        resp.raise_for_status()
        return resp.json()["access_token"]


# ── Google Drive ───────────────────────────────────────────────────────────

async def drive_list_files(query: str = "", max_results: int = 10) -> str:
    if not config.GOOGLE_REFRESH_TOKEN:
        return "Google Drive não configurado — adicione GOOGLE_REFRESH_TOKEN no Railway."
    try:
        token = await _google_access_token()
        params = {
            "pageSize": max_results,
            "fields": "files(id,name,mimeType,modifiedTime,size)",
            "orderBy": "modifiedTime desc",
        }
        if query:
            params["q"] = f"name contains '{query}'"
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                "https://www.googleapis.com/drive/v3/files",
                params=params,
                headers={"Authorization": f"Bearer {token}"},
            )
            resp.raise_for_status()
            files = resp.json().get("files", [])
        if not files:
            return "Nenhum arquivo encontrado no Google Drive."
        lines = [f"📁 **Google Drive** — {len(files)} arquivo(s):\n"]
        for f in files:
            size = int(f.get("size", 0))
            size_str = f"{size // 1024} KB" if size > 1024 else f"{size} B" if size else "—"
            lines.append(f"• **{f['name']}** ({size_str}) — `{f['id']}`")
        return "\n".join(lines)
    except Exception as exc:
        return f"Erro ao listar arquivos do Drive: {exc}"


async def drive_read_file(file_id: str) -> str:
    if not config.GOOGLE_REFRESH_TOKEN:
        return "Google Drive não configurado."
    try:
        token = await _google_access_token()
        async with httpx.AsyncClient(timeout=20.0) as client:
            meta_resp = await client.get(
                f"https://www.googleapis.com/drive/v3/files/{file_id}",
                params={"fields": "name,mimeType"},
                headers={"Authorization": f"Bearer {token}"},
            )
            meta_resp.raise_for_status()
            meta = meta_resp.json()
            mime = meta.get("mimeType", "")
            name = meta.get("name", file_id)

            if "google-apps" in mime:
                export_mime = "text/plain"
                dl_resp = await client.get(
                    f"https://www.googleapis.com/drive/v3/files/{file_id}/export",
                    params={"mimeType": export_mime},
                    headers={"Authorization": f"Bearer {token}"},
                )
            else:
                dl_resp = await client.get(
                    f"https://www.googleapis.com/drive/v3/files/{file_id}",
                    params={"alt": "media"},
                    headers={"Authorization": f"Bearer {token}"},
                )
            dl_resp.raise_for_status()
            content = dl_resp.text[:3000]
        return f"📄 **{name}**\n\n{content}"
    except Exception as exc:
        return f"Erro ao ler arquivo do Drive: {exc}"


# ── Gmail ──────────────────────────────────────────────────────────────────

async def gmail_list(max_results: int = 5, query: str = "") -> str:
    if not config.GOOGLE_REFRESH_TOKEN:
        return "Gmail não configurado — adicione GOOGLE_REFRESH_TOKEN no Railway."
    try:
        token = await _google_access_token()
        params = {"maxResults": max_results, "q": query or "is:unread"}
        async with httpx.AsyncClient(timeout=15.0) as client:
            list_resp = await client.get(
                "https://gmail.googleapis.com/gmail/v1/users/me/messages",
                params=params,
                headers={"Authorization": f"Bearer {token}"},
            )
            list_resp.raise_for_status()
            messages = list_resp.json().get("messages", [])
            if not messages:
                return "Nenhum email encontrado."
            lines = [f"📧 **Gmail** — {len(messages)} email(s):\n"]
            for msg in messages:
                detail = await client.get(
                    f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg['id']}",
                    params={"format": "metadata", "metadataHeaders": ["Subject", "From", "Date"]},
                    headers={"Authorization": f"Bearer {token}"},
                )
                detail.raise_for_status()
                headers = {h["name"]: h["value"] for h in detail.json().get("payload", {}).get("headers", [])}
                lines.append(f"• **{headers.get('Subject', '(sem assunto)')}**")
                lines.append(f"  De: {headers.get('From', '?')} | {headers.get('Date', '')[:16]}")
        return "\n".join(lines)
    except Exception as exc:
        return f"Erro ao listar emails: {exc}"


async def gmail_send(to: str, subject: str, body: str) -> str:
    if not config.GOOGLE_REFRESH_TOKEN:
        return "Gmail não configurado."
    try:
        import base64
        from email.mime.text import MIMEText
        token = await _google_access_token()
        msg = MIMEText(body)
        msg["to"] = to
        msg["subject"] = subject
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(
                "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
                json={"raw": raw},
                headers={"Authorization": f"Bearer {token}"},
            )
            resp.raise_for_status()
        return f"✅ Email enviado para {to} com sucesso!"
    except Exception as exc:
        return f"Erro ao enviar email: {exc}"


# ── Financial Movements ────────────────────────────────────────────────────

async def tool_add_movement(movement_type: str, amount: float, description: str, category: str = "geral") -> str:
    from memory import add_movement as db_add
    tipo = movement_type.lower().strip().replace("saída", "saida")
    if tipo not in ("entrada", "saida"):
        return "Tipo inválido. Use 'entrada' (recebimento) ou 'saida' (gasto/pagamento)."
    if amount <= 0:
        return "Valor deve ser maior que zero."
    mov_id = db_add(tipo, amount, description, category)
    emoji = "💰" if tipo == "entrada" else "💸"
    sinal = "+" if tipo == "entrada" else "-"
    return (
        f"{emoji} **Movimento registrado!**\n\n"
        f"**#{mov_id}** — {description}\n"
        f"**Tipo:** {tipo.capitalize()}\n"
        f"**Valor:** {sinal}R$ {amount:,.2f}\n"
        f"**Categoria:** {category}"
    )


async def tool_list_movements(limit: int = 10, category: str = "") -> str:
    from memory import list_movements as db_list, get_balance as db_balance
    movements = db_list(limit=limit, category=category if category else None)
    balance = db_balance()

    saldo_emoji = "📈" if balance["saldo"] >= 0 else "📉"
    lines = [
        f"📊 **Extrato — últimos {len(movements)} movimentos**\n",
        f"💰 Entradas totais: R$ {balance['entradas']:,.2f}",
        f"💸 Saídas totais:   R$ {balance['saidas']:,.2f}",
        f"{saldo_emoji} **Saldo atual:     R$ {balance['saldo']:,.2f}**\n",
        "---",
    ]

    if not movements:
        lines.append("_Nenhum movimento registrado ainda._")
    else:
        for m in movements:
            emoji = "↗️" if m["type"] == "entrada" else "↘️"
            sinal = "+" if m["type"] == "entrada" else "-"
            data = m["created_at"][:10]
            lines.append(
                f"{emoji} **{sinal}R$ {m['amount']:,.2f}** — {m['description']} "
                f"`[{m['category']}]` _{data}_"
            )

    return "\n".join(lines)


async def tool_get_balance() -> str:
    from memory import get_balance as db_balance
    b = db_balance()
    saldo_emoji = "📈" if b["saldo"] >= 0 else "📉"
    return (
        f"💵 **Saldo Atual**\n\n"
        f"💰 Entradas: **R$ {b['entradas']:,.2f}**\n"
        f"💸 Saídas:   **R$ {b['saidas']:,.2f}**\n"
        f"{saldo_emoji} Saldo:    **R$ {b['saldo']:,.2f}**\n\n"
        f"_Total de {b['total_movimentos']} movimentos registrados_"
    )


# ── Claude tool definitions ────────────────────────────────────────────────

def format_tools_for_claude() -> list[dict]:
    return [
        {
            "name": "get_current_datetime",
            "description": (
                "Retorna a data e hora atual no fuso horário de Brasília. "
                "Use quando o usuário perguntar que horas são, qual é a data de hoje, etc."
            ),
            "input_schema": {"type": "object", "properties": {}, "required": []},
        },
        {
            "name": "calculate",
            "description": (
                "Calcula expressões matemáticas com segurança. "
                "Suporta operações básicas (+, -, *, /), potência (**), raiz quadrada (sqrt), "
                "logarítmos, funções trigonométricas e constantes pi e e."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Expressão matemática. Ex: '2 ** 10', 'sqrt(144) + 5 * 3'"}
                },
                "required": ["expression"],
            },
        },
        {
            "name": "web_search",
            "description": (
                "Busca informações atualizadas na internet via Tavily. "
                "Use para notícias recentes, preços, tendências de mercado, ou qualquer dado atual."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Consulta de busca em linguagem natural."}
                },
                "required": ["query"],
            },
        },
        {
            "name": "create_file_content",
            "description": (
                "Gera conteúdo formatado como arquivo para o usuário baixar ou copiar. "
                "Use quando pedirem para criar scripts, documentos, templates, etc."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Nome do arquivo com extensão."},
                    "content": {"type": "string", "description": "Conteúdo completo do arquivo."},
                    "file_type": {"type": "string", "description": "Tipo para syntax highlight: python, markdown, json, etc.", "default": "text"},
                },
                "required": ["filename", "content"],
            },
        },
        {
            "name": "generate_pony_digital_content",
            "description": (
                "Gera conteúdo de marketing para o negócio Pony-Digital de Ramon: "
                "hooks para Instagram, captions, emails de vendas, CTAs e headlines."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "content_type": {"type": "string", "description": "Tipo: hook, caption, email, cta, ou headline", "enum": ["hook", "caption", "email", "cta", "headline"]},
                    "topic": {"type": "string", "description": "Tema. Ex: 'planilhas', 'finanças', 'produtividade'"},
                },
                "required": ["content_type", "topic"],
            },
        },
        {
            "name": "get_weather",
            "description": (
                "Consulta a previsão do tempo em tempo real para qualquer cidade. "
                "Retorna temperatura atual, máxima, mínima, condição e vento. "
                "Use sempre que Ramon perguntar sobre o clima ou tempo."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Nome da cidade. Ex: 'São Paulo', 'Rio de Janeiro', 'Belo Horizonte'"}
                },
                "required": ["city"],
            },
        },
        {
            "name": "youtube_search",
            "description": (
                "Busca vídeos no YouTube por palavra-chave. "
                "Use quando Ramon pedir para encontrar vídeos, tutoriais, ou conteúdo no YouTube."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Termo de busca. Ex: 'como montar PC gamer', 'planilhas Excel'"},
                    "max_results": {"type": "integer", "description": "Número de resultados (1-10). Padrão: 5.", "default": 5},
                },
                "required": ["query"],
            },
        },
        {
            "name": "youtube_channel_stats",
            "description": (
                "Retorna estatísticas de um canal do YouTube: inscritos, visualizações e vídeos publicados. "
                "Use quando Ramon quiser ver dados do próprio canal ou de qualquer outro canal."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "channel_id": {"type": "string", "description": "ID do canal YouTube (formato UCxxxxxxxx)."},
                },
                "required": ["channel_id"],
            },
        },
        {
            "name": "add_movement",
            "description": (
                "Registra uma movimentação financeira (entrada ou saída). "
                "Use quando Ramon disser que recebeu, vendeu, ganhou, gastou, pagou ou transferiu algum valor."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "movement_type": {
                        "type": "string",
                        "description": "'entrada' para recebimentos/vendas, 'saida' para gastos/pagamentos.",
                        "enum": ["entrada", "saida"],
                    },
                    "amount": {"type": "number", "description": "Valor em reais. Apenas o número, sem R$."},
                    "description": {"type": "string", "description": "Descrição do movimento. Ex: 'Venda planilha Kiwify', 'Internet mensal', 'Salário'"},
                    "category": {"type": "string", "description": "Categoria opcional. Ex: 'kiwify', 'contas', 'marketing', 'salário'. Padrão: 'geral'", "default": "geral"},
                },
                "required": ["movement_type", "amount", "description"],
            },
        },
        {
            "name": "list_movements",
            "description": (
                "Lista os movimentos financeiros registrados e mostra o saldo atual. "
                "Use quando Ramon quiser ver o extrato, os gastos recentes, as entradas ou consultar o histórico."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Quantos movimentos mostrar (padrão: 10).", "default": 10},
                    "category": {"type": "string", "description": "Filtrar por categoria. Deixe vazio para ver todos.", "default": ""},
                },
                "required": [],
            },
        },
        {
            "name": "get_balance",
            "description": (
                "Mostra o saldo atual: total de entradas, saídas e saldo líquido. "
                "Use quando Ramon perguntar quanto tem, qual o saldo, como está o caixa."
            ),
            "input_schema": {"type": "object", "properties": {}, "required": []},
        },
        {
            "name": "facebook_instagram_stats",
            "description": (
                "Consulta estatísticas da página do Facebook e do Instagram de Ramon em tempo real. "
                "Retorna curtidas e seguidores do Facebook, e seguidores e posts do Instagram. "
                "Use quando Ramon perguntar sobre seguidores, curtidas, stats das redes sociais, Instagram ou Facebook."
            ),
            "input_schema": {"type": "object", "properties": {}, "required": []},
        },
        {
            "name": "drive_list_files",
            "description": (
                "Lista arquivos do Google Drive de Ramon. "
                "Use quando ele perguntar sobre arquivos no Drive, quiser buscar documentos ou ver o que tem salvo."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Termo de busca pelo nome do arquivo. Deixe vazio para listar os mais recentes.", "default": ""},
                    "max_results": {"type": "integer", "description": "Quantidade máxima de arquivos (padrão: 10).", "default": 10},
                },
                "required": [],
            },
        },
        {
            "name": "drive_read_file",
            "description": (
                "Lê o conteúdo de um arquivo do Google Drive pelo ID. "
                "Use após listar os arquivos para ler um específico."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "file_id": {"type": "string", "description": "ID do arquivo no Google Drive."},
                },
                "required": ["file_id"],
            },
        },
        {
            "name": "gmail_list",
            "description": (
                "Lista emails do Gmail de Ramon. "
                "Use quando ele quiser ver emails, checar a caixa de entrada ou buscar mensagens."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "max_results": {"type": "integer", "description": "Quantidade de emails (padrão: 5).", "default": 5},
                    "query": {"type": "string", "description": "Filtro de busca estilo Gmail. Ex: 'is:unread', 'from:alguem@gmail.com', 'subject:reunião'. Padrão: 'is:unread'", "default": ""},
                },
                "required": [],
            },
        },
        {
            "name": "gmail_send",
            "description": (
                "Envia um email pelo Gmail de Ramon. "
                "Use quando ele pedir para enviar um email, responder alguém ou mandar mensagem."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Endereço de email do destinatário."},
                    "subject": {"type": "string", "description": "Assunto do email."},
                    "body": {"type": "string", "description": "Corpo do email em texto simples."},
                },
                "required": ["to", "subject", "body"],
            },
        },
        {
            "name": "system_info",
            "description": "Retorna informações do servidor em tempo real: CPU, RAM, disco e tempo ligado. Use quando Ramon perguntar sobre o status do servidor ou recursos.",
            "input_schema": {"type": "object", "properties": {}, "required": []},
        },
        {
            "name": "run_command",
            "description": "Executa um comando de terminal no servidor Linux. Use para operações de sistema, instalar pacotes, verificar processos, etc.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Comando shell a executar."},
                    "timeout": {"type": "integer", "description": "Timeout em segundos (padrão: 30).", "default": 30},
                },
                "required": ["command"],
            },
        },
        {
            "name": "list_files",
            "description": "Lista os arquivos e pastas de um diretório no servidor.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Caminho do diretório. Ex: '/app', '/data'"}
                },
                "required": ["path"],
            },
        },
        {
            "name": "read_file",
            "description": "Lê e retorna o conteúdo de um arquivo no servidor.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Caminho completo do arquivo."}
                },
                "required": ["path"],
            },
        },
        {
            "name": "write_file",
            "description": "Cria ou sobrescreve um arquivo no servidor com o conteúdo fornecido.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Caminho completo do arquivo."},
                    "content": {"type": "string", "description": "Conteúdo a escrever no arquivo."},
                },
                "required": ["path", "content"],
            },
        },
        {
            "name": "take_screenshot",
            "description": (
                "Tira um screenshot de qualquer URL usando o browser headless. "
                "Use quando Ramon pedir para ver uma página, verificar um site, "
                "ou quando precisar visualizar conteúdo de uma URL."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL completa para capturar. Ex: 'https://kiwify.com.br'"},
                    "full_page": {"type": "boolean", "description": "Se True, captura a página inteira.", "default": False},
                },
                "required": ["url"],
            },
        },
        {
            "name": "browse_and_read",
            "description": (
                "Abre uma URL e lê o conteúdo de texto da página. "
                "Use para extrair informações de sites, artigos, preços, etc."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL para acessar e ler."}
                },
                "required": ["url"],
            },
        },
        {
            "name": "trigger_n8n",
            "description": (
                "Aciona um fluxo de automação no n8n. Use para executar tarefas automáticas "
                "como postar em redes sociais, enviar emails, buscar dados externos, "
                "processar informações, ou qualquer outra automação configurada no n8n. "
                "Especifique a ação desejada e os dados necessários."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "Nome da ação a executar. Ex: 'postar_instagram', 'enviar_email', 'buscar_dados'."
                    },
                    "data": {
                        "type": "object",
                        "description": "Dados necessários para a automação. Ex: {'mensagem': 'Texto do post', 'destinatario': 'email@exemplo.com'}."
                    },
                },
                "required": ["action"],
            },
        },
    ]


async def trigger_n8n(action: str, data: dict = {}) -> str:
    n8n_url = os.getenv("N8N_WEBHOOK_URL", "https://n8n-production-fea4.up.railway.app/webhook/818e253f-0228-474a-8b6d-eff3b5f0bcc8")
    payload = {"action": action, "data": data}
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(n8n_url, json=payload)
            response.raise_for_status()
            result = response.json()
            return f"Automação '{action}' executada com sucesso. Resultado: {result}"
    except httpx.TimeoutException:
        return f"Automação '{action}' demorou demais para responder. Tente novamente."
    except httpx.HTTPStatusError as exc:
        return f"Erro na automação '{action}' (HTTP {exc.response.status_code})."
    except Exception as exc:
        return f"Erro ao acionar automação '{action}': {exc}"


# ── Tool dispatcher ──────────────────────────────────────────────────────

async def process_tool_call(tool_name: str, tool_input: dict, config: Any):
    try:
        if tool_name == "get_current_datetime":
            return await get_current_datetime()
        elif tool_name == "calculate":
            return await calculate(tool_input.get("expression", ""))
        elif tool_name == "web_search":
            return await web_search(query=tool_input.get("query", ""), api_key=config.TAVILY_API_KEY)
        elif tool_name == "create_file_content":
            return await create_file_content(
                filename=tool_input.get("filename", "arquivo.txt"),
                content=tool_input.get("content", ""),
                file_type=tool_input.get("file_type", "text"),
            )
        elif tool_name == "generate_pony_digital_content":
            return await generate_pony_digital_content(
                content_type=tool_input.get("content_type", "caption"),
                topic=tool_input.get("topic", "negócios digitais"),
            )
        elif tool_name == "get_weather":
            return await get_weather(tool_input.get("city", ""))
        elif tool_name == "youtube_search":
            return await youtube_search(
                query=tool_input.get("query", ""),
                api_key=config.YOUTUBE_API_KEY,
                max_results=tool_input.get("max_results", 5),
            )
        elif tool_name == "youtube_channel_stats":
            return await youtube_channel_stats(
                channel_id=tool_input.get("channel_id", ""),
                api_key=config.YOUTUBE_API_KEY,
            )
        elif tool_name == "add_movement":
            return await tool_add_movement(
                movement_type=tool_input.get("movement_type", "entrada"),
                amount=float(tool_input.get("amount", 0)),
                description=tool_input.get("description", ""),
                category=tool_input.get("category", "geral"),
            )
        elif tool_name == "list_movements":
            return await tool_list_movements(
                limit=tool_input.get("limit", 10),
                category=tool_input.get("category", ""),
            )
        elif tool_name == "get_balance":
            return await tool_get_balance()
        elif tool_name == "facebook_instagram_stats":
            return await facebook_instagram_stats(
                token=config.FACEBOOK_PAGE_TOKEN,
                page_id=config.FACEBOOK_PAGE_ID,
            )
        elif tool_name == "drive_list_files":
            return await drive_list_files(
                query=tool_input.get("query", ""),
                max_results=tool_input.get("max_results", 10),
            )
        elif tool_name == "drive_read_file":
            return await drive_read_file(file_id=tool_input.get("file_id", ""))
        elif tool_name == "gmail_list":
            return await gmail_list(
                max_results=tool_input.get("max_results", 5),
                query=tool_input.get("query", ""),
            )
        elif tool_name == "gmail_send":
            return await gmail_send(
                to=tool_input.get("to", ""),
                subject=tool_input.get("subject", ""),
                body=tool_input.get("body", ""),
            )
        elif tool_name == "system_info":
            return await system_info()
        elif tool_name == "run_command":
            return await run_command(
                command=tool_input.get("command", ""),
                timeout=tool_input.get("timeout", 30),
            )
        elif tool_name == "list_files":
            return await list_files(tool_input.get("path", "/app"))
        elif tool_name == "read_file":
            return await read_file(tool_input.get("path", ""))
        elif tool_name == "write_file":
            return await write_file(
                path=tool_input.get("path", ""),
                content=tool_input.get("content", ""),
            )
        elif tool_name == "take_screenshot":
            return await take_screenshot(
                url=tool_input.get("url", ""),
                full_page=tool_input.get("full_page", False),
            )
        elif tool_name == "browse_and_read":
            return await browse_and_read(url=tool_input.get("url", ""))
        elif tool_name == "trigger_n8n":
            return await trigger_n8n(
                action=tool_input.get("action", ""),
                data=tool_input.get("data", {}),
            )
        else:
            return f"Ferramenta desconhecida: '{tool_name}'."
    except Exception as exc:
        return f"Erro ao executar '{tool_name}': {exc}"
