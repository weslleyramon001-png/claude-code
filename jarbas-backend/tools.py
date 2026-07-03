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


async def tool_create_reminder(title: str, description: str = "", due_date: str = "") -> str:
    from memory import create_reminder as db_create
    rid = db_create(title, description, due_date)
    parts = [f"📌 **Lembrete criado!**\n\n**#{rid}** — {title}"]
    if description:
        parts.append(f"📝 {description}")
    if due_date:
        parts.append(f"📅 Prazo: {due_date}")
    return "\n".join(parts)


async def tool_list_reminders(include_completed: bool = False) -> str:
    from memory import list_reminders as db_list
    items = db_list(include_completed)
    if not items:
        return "Nenhum lembrete pendente, Ramon."
    label = " (incluindo concluídos)" if include_completed else ""
    lines = [f"📋 **Lembretes{label}** — {len(items)} item(s)\n"]
    for r in items:
        status = "✅" if r["completed"] else "⏳"
        due = f" · 📅 {r['due_date']}" if r.get("due_date") else ""
        desc = f"\n   ↳ {r['description']}" if r.get("description") else ""
        lines.append(f"{status} **#{r['id']}** {r['title']}{due}{desc}")
    return "\n".join(lines)


async def tool_complete_reminder(reminder_id: int) -> str:
    from memory import complete_reminder as db_complete
    success = db_complete(reminder_id)
    if success:
        return f"✅ Lembrete #{reminder_id} marcado como concluído!"
    return f"Lembrete #{reminder_id} não encontrado ou já estava concluído."


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


async def tool_save_memory(category: str, fact: str) -> str:
    from memory import save_fact
    save_fact(category.lower().strip(), fact.strip())
    return f"🧠 Memorizado em [{category.upper()}]: {fact}"


async def tool_list_memories() -> str:
    from memory import get_facts_with_ids
    facts = get_facts_with_ids()
    if not facts:
        return "Nenhuma memória salva ainda."
    current_cat = None
    lines = ["🧠 **Memórias do JARBAS**\n"]
    for f in facts:
        if f["category"] != current_cat:
            current_cat = f["category"]
            lines.append(f"\n**[{current_cat.upper()}]**")
        lines.append(f"  #{f['id']} — {f['fact']}")
    return "\n".join(lines)


async def tool_delete_memory(fact_id: int) -> str:
    from memory import delete_fact
    success = delete_fact(fact_id)
    if success:
        return f"🗑️ Memória #{fact_id} apagada."
    return f"Memória #{fact_id} não encontrada."


# ── YouTube ────────────────────────────────────────────────────────────────

async def _resolve_channel_id(client: httpx.AsyncClient, channel_id: str, api_key: str) -> str:
    """Resolve @handle para channel ID usando forHandle (1 quota unit, não 100)."""
    if not channel_id.startswith("@"):
        return channel_id
    handle = channel_id.lstrip("@")
    resp = await client.get(
        "https://www.googleapis.com/youtube/v3/channels",
        params={"part": "id", "forHandle": handle, "key": api_key},
    )
    resp.raise_for_status()
    items = resp.json().get("items", [])
    if not items:
        raise ValueError(f"Canal '{channel_id}' não encontrado no YouTube.")
    return items[0]["id"]


def _youtube_error(exc: httpx.HTTPStatusError) -> str:
    try:
        reason = exc.response.json()["error"]["errors"][0].get("reason", "")
        message = exc.response.json()["error"].get("message", "")
    except Exception:
        reason, message = "", ""
    if exc.response.status_code == 403:
        if "quotaExceeded" in reason:
            return "Quota diária da YouTube API esgotada (10.000 unidades/dia). Tente amanhã."
        if "keyInvalid" in reason:
            return "Chave da YouTube API inválida. Verifique YOUTUBE_API_KEY no Railway."
        if "accessNotConfigured" in reason:
            return "YouTube Data API v3 não está habilitada para esta chave. Ative no Google Cloud Console."
        return f"YouTube API bloqueou a requisição (403). Verifique restrições de IP/chave no Google Cloud Console. Detalhe: {message or reason}"
    return f"Erro YouTube API (HTTP {exc.response.status_code}): {message}"


async def get_youtube_channel_stats(channel_alias: str, api_key: str, channels_config: list) -> str:
    if not api_key:
        return "YouTube API não configurada. Adicione YOUTUBE_API_KEY no Railway."

    channel_id = None
    for ch in channels_config:
        if ch.get("alias") == channel_alias:
            channel_id = ch.get("channel_id")
            break

    if not channel_id:
        aliases = [c.get("alias") for c in channels_config]
        return f"Canal '{channel_alias}' não encontrado. Aliases disponíveis: {aliases}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            channel_id = await _resolve_channel_id(client, channel_id, api_key)

            stats_resp = await client.get(
                "https://www.googleapis.com/youtube/v3/channels",
                params={"part": "snippet,statistics", "id": channel_id, "key": api_key},
            )
            stats_resp.raise_for_status()
            items = stats_resp.json().get("items", [])
            if not items:
                return "Canal não encontrado."

            ch = items[0]
            name = ch["snippet"]["title"]
            desc = ch["snippet"].get("description", "")[:200]
            stats = ch["statistics"]
            subs = int(stats.get("subscriberCount", 0))
            views = int(stats.get("viewCount", 0))
            videos = int(stats.get("videoCount", 0))

            return (
                f"📺 **{name}**\n\n"
                f"👥 Inscritos: **{subs:,}**\n"
                f"👁️ Views totais: **{views:,}**\n"
                f"🎬 Vídeos publicados: **{videos}**\n\n"
                f"_{desc}_"
            )
    except ValueError as exc:
        return str(exc)
    except httpx.HTTPStatusError as exc:
        return _youtube_error(exc)
    except Exception as exc:
        return f"Erro ao consultar YouTube: {exc}"


async def get_youtube_recent_videos(channel_alias: str, api_key: str, channels_config: list, max_results: int = 5) -> str:
    if not api_key:
        return "YouTube API não configurada. Adicione YOUTUBE_API_KEY no Railway."

    channel_id = None
    for ch in channels_config:
        if ch.get("alias") == channel_alias:
            channel_id = ch.get("channel_id")
            break

    if not channel_id:
        aliases = [c.get("alias") for c in channels_config]
        return f"Canal '{channel_alias}' não encontrado. Aliases disponíveis: {aliases}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            channel_id = await _resolve_channel_id(client, channel_id, api_key)

            videos_resp = await client.get(
                "https://www.googleapis.com/youtube/v3/search",
                params={
                    "part": "snippet", "channelId": channel_id, "type": "video",
                    "order": "date", "maxResults": max_results, "key": api_key,
                },
            )
            videos_resp.raise_for_status()
            items = videos_resp.json().get("items", [])
            if not items:
                return "Nenhum vídeo encontrado no canal."

            video_ids = [i["id"]["videoId"] for i in items]
            stats_resp = await client.get(
                "https://www.googleapis.com/youtube/v3/videos",
                params={"part": "statistics,contentDetails", "id": ",".join(video_ids), "key": api_key},
            )
            stats_resp.raise_for_status()
            stats_map = {v["id"]: v for v in stats_resp.json().get("items", [])}

            lines = [f"🎬 **Últimos {len(items)} vídeos**\n"]
            for item in items:
                vid_id = item["id"]["videoId"]
                title = item["snippet"]["title"]
                published = item["snippet"]["publishedAt"][:10]
                url = f"https://youtube.com/watch?v={vid_id}"
                vstats = stats_map.get(vid_id, {}).get("statistics", {})
                views = int(vstats.get("viewCount", 0))
                likes = int(vstats.get("likeCount", 0))
                lines.append(f"▶️ **{title}**")
                lines.append(f"   👁️ {views:,} views · 👍 {likes:,} likes · 📅 {published}")
                lines.append(f"   {url}\n")

            return "\n".join(lines)
    except ValueError as exc:
        return str(exc)
    except httpx.HTTPStatusError as exc:
        return _youtube_error(exc)
    except Exception as exc:
        return f"Erro ao buscar vídeos: {exc}"


# ── Meta (Facebook + Instagram) ────────────────────────────────────────────

_GRAPH_BASE = "https://graph.facebook.com/v19.0"


def _meta_error(exc: httpx.HTTPStatusError) -> str:
    try:
        error = exc.response.json().get("error", {})
        message = error.get("message", "")
        code = error.get("code", 0)
    except Exception:
        message, code = "", 0
    if exc.response.status_code == 401 or code == 190:
        return "Token Meta expirado ou inválido. Gere um novo Page Access Token no Graph API Explorer."
    if code == 200:
        return "Permissão negada pelo Meta. Verifique as permissões do app no Graph API Explorer."
    if code in (4, 32):
        return "Limite de chamadas da API Meta atingido. Aguarde alguns minutos."
    return f"Erro Meta API (HTTP {exc.response.status_code}, code {code}): {message}"


async def get_facebook_page_stats(page_id: str, page_access_token: str) -> str:
    if not page_access_token:
        return "Meta não configurada. Adicione META_PAGE_ACCESS_TOKEN no Railway."
    if not page_id:
        return "META_PAGE_ID não configurado no Railway."
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{_GRAPH_BASE}/{page_id}",
                params={
                    "fields": "name,fan_count,followers_count,about,website",
                    "access_token": page_access_token,
                },
            )
            resp.raise_for_status()
            data = resp.json()
        name = data.get("name", "?")
        fans = data.get("fan_count", 0)
        followers = data.get("followers_count", 0)
        about = data.get("about", "")
        website = data.get("website", "")
        lines = [
            f"📘 **{name}** (Facebook Page)",
            f"👥 Curtidas: **{fans:,}**",
            f"👥 Seguidores: **{followers:,}**",
        ]
        if about:
            lines.append(f"📝 {about}")
        if website:
            lines.append(f"🔗 {website}")
        return "\n".join(lines)
    except httpx.HTTPStatusError as exc:
        return _meta_error(exc)
    except Exception as exc:
        return f"Erro ao consultar página do Facebook: {exc}"


async def get_instagram_profile(ig_user_id: str, page_access_token: str) -> str:
    if not page_access_token:
        return "Meta não configurada. Adicione META_PAGE_ACCESS_TOKEN no Railway."
    if not ig_user_id:
        return "META_IG_USER_ID não configurado no Railway."
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{_GRAPH_BASE}/{ig_user_id}",
                params={
                    "fields": "name,username,biography,followers_count,follows_count,media_count,website",
                    "access_token": page_access_token,
                },
            )
            resp.raise_for_status()
            data = resp.json()
        username = data.get("username", "?")
        name = data.get("name", "?")
        bio = data.get("biography", "")
        followers = data.get("followers_count", 0)
        following = data.get("follows_count", 0)
        posts = data.get("media_count", 0)
        website = data.get("website", "")
        lines = [
            f"📸 **@{username}** ({name})",
            f"👥 Seguidores: **{followers:,}**",
            f"➡️ Seguindo: **{following:,}**",
            f"🖼️ Publicações: **{posts}**",
        ]
        if bio:
            lines.append(f"📝 {bio}")
        if website:
            lines.append(f"🔗 {website}")
        return "\n".join(lines)
    except httpx.HTTPStatusError as exc:
        return _meta_error(exc)
    except Exception as exc:
        return f"Erro ao consultar Instagram: {exc}"


async def get_instagram_recent_posts(ig_user_id: str, page_access_token: str, limit: int = 5) -> str:
    if not page_access_token:
        return "Meta não configurada. Adicione META_PAGE_ACCESS_TOKEN no Railway."
    if not ig_user_id:
        return "META_IG_USER_ID não configurado no Railway."
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{_GRAPH_BASE}/{ig_user_id}/media",
                params={
                    "fields": "id,caption,media_type,timestamp,like_count,comments_count,permalink",
                    "limit": limit,
                    "access_token": page_access_token,
                },
            )
            resp.raise_for_status()
            items = resp.json().get("data", [])
        if not items:
            return "Nenhuma publicação encontrada no Instagram."
        lines = [f"📸 **Últimas {len(items)} publicações no Instagram**\n"]
        type_icon = {"IMAGE": "🖼️", "VIDEO": "🎬", "CAROUSEL_ALBUM": "📂"}
        for post in items:
            caption = (post.get("caption") or "")[:120].replace("\n", " ")
            if len(post.get("caption") or "") > 120:
                caption += "..."
            icon = type_icon.get(post.get("media_type", ""), "📄")
            ts = post.get("timestamp", "")[:10]
            likes = post.get("like_count", 0)
            comments = post.get("comments_count", 0)
            permalink = post.get("permalink", "")
            lines.append(f"{icon} _{ts}_ · 👍 **{likes}** · 💬 **{comments}**")
            if caption:
                lines.append(f"   \"{caption}\"")
            if permalink:
                lines.append(f"   {permalink}")
            lines.append("")
        return "\n".join(lines)
    except httpx.HTTPStatusError as exc:
        return _meta_error(exc)
    except Exception as exc:
        return f"Erro ao buscar posts do Instagram: {exc}"


async def post_to_facebook(message: str, page_id: str, page_access_token: str) -> str:
    if not page_access_token:
        return "Meta não configurada. Adicione META_PAGE_ACCESS_TOKEN no Railway."
    if not page_id:
        return "META_PAGE_ID não configurado no Railway."
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(
                f"{_GRAPH_BASE}/{page_id}/feed",
                data={"message": message, "access_token": page_access_token},
            )
            resp.raise_for_status()
            post_id = resp.json().get("id", "?")
        preview = message[:200] + ("..." if len(message) > 200 else "")
        return f"✅ **Publicado no Facebook!**\n\nID: `{post_id}`\n\n> {preview}"
    except httpx.HTTPStatusError as exc:
        return _meta_error(exc)
    except Exception as exc:
        return f"Erro ao publicar no Facebook: {exc}"


async def post_to_instagram(ig_user_id: str, page_access_token: str, image_url: str, caption: str = "") -> str:
    if not page_access_token:
        return "Meta não configurada. Adicione META_PAGE_ACCESS_TOKEN no Railway."
    if not ig_user_id:
        return "META_IG_USER_ID não configurado no Railway."
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            container_resp = await client.post(
                f"{_GRAPH_BASE}/{ig_user_id}/media",
                data={"image_url": image_url, "caption": caption, "access_token": page_access_token},
            )
            container_resp.raise_for_status()
            creation_id = container_resp.json().get("id")
            if not creation_id:
                return "Erro: container de mídia não foi criado. Verifique se a URL da imagem é pública."

            publish_resp = await client.post(
                f"{_GRAPH_BASE}/{ig_user_id}/media_publish",
                data={"creation_id": creation_id, "access_token": page_access_token},
            )
            publish_resp.raise_for_status()
            media_id = publish_resp.json().get("id", "?")

        preview_caption = caption[:200] + ("..." if len(caption) > 200 else "") if caption else "(sem legenda)"
        return (
            f"✅ **Publicado no Instagram!**\n\n"
            f"ID: `{media_id}`\n"
            f"📸 Imagem: {image_url[:80]}\n"
            f"📝 {preview_caption}"
        )
    except httpx.HTTPStatusError as exc:
        return _meta_error(exc)
    except Exception as exc:
        return f"Erro ao publicar no Instagram: {exc}"


# ── IXC Soft — Servlink Telecom ───────────────────────────────────────────

async def tool_ixc_login(ixc_email: str, ixc_password: str, two_fa_code: str = "") -> str:
    from ixc import ixc_login
    return await ixc_login(ixc_email, ixc_password, two_fa_code)


async def tool_ixc_get_onus_rede_neutra(ixc_email: str, ixc_password: str, limit: int = 100) -> str:
    from ixc import ixc_get_onus_rede_neutra
    return await ixc_get_onus_rede_neutra(ixc_email, ixc_password, limit)


async def tool_ixc_get_onus_online_por_vlan(ixc_email: str, ixc_password: str, vlan: str = "") -> str:
    from ixc import ixc_get_onus_online_por_vlan
    return await ixc_get_onus_online_por_vlan(ixc_email, ixc_password, vlan)


async def tool_ixc_screenshot(ixc_email: str, ixc_password: str) -> dict:
    from ixc import ixc_screenshot
    return await ixc_screenshot(ixc_email, ixc_password)


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
            "name": "create_reminder",
            "description": (
                "Cria um lembrete para Ramon. Use quando ele pedir para lembrar de algo, "
                "agendar uma tarefa ou registrar um prazo."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Título do lembrete."},
                    "description": {"type": "string", "description": "Detalhes adicionais (opcional).", "default": ""},
                    "due_date": {"type": "string", "description": "Data/prazo (opcional). Ex: '2026-07-18', 'antes de julho'.", "default": ""},
                },
                "required": ["title"],
            },
        },
        {
            "name": "list_reminders",
            "description": (
                "Lista os lembretes pendentes de Ramon. "
                "Use quando ele perguntar o que tem para fazer, quais são os lembretes, etc."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "include_completed": {"type": "boolean", "description": "Se True, inclui lembretes já concluídos.", "default": False},
                },
                "required": [],
            },
        },
        {
            "name": "complete_reminder",
            "description": "Marca um lembrete como concluído pelo ID.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "reminder_id": {"type": "integer", "description": "ID do lembrete a concluir."},
                },
                "required": ["reminder_id"],
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
            "name": "save_memory",
            "description": (
                "Salva um fato importante sobre Ramon na memória persistente do JARBAS. "
                "Use sempre que Ramon revelar algo relevante: preferências, metas, contexto de negócio, "
                "decisões tomadas, informações pessoais ou qualquer coisa que deva ser lembrada no futuro."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Categoria do fato. Ex: 'identity', 'business', 'goals', 'preferences', 'finance', 'projects'.",
                    },
                    "fact": {
                        "type": "string",
                        "description": "O fato a memorizar, escrito de forma clara e objetiva. Ex: 'Prefere respostas curtas e diretas.'",
                    },
                },
                "required": ["category", "fact"],
            },
        },
        {
            "name": "list_memories",
            "description": (
                "Lista todas as memórias salvas sobre Ramon. "
                "Use quando Ramon perguntar o que o JARBAS sabe sobre ele, ou antes de salvar algo novo para evitar duplicatas."
            ),
            "input_schema": {"type": "object", "properties": {}, "required": []},
        },
        {
            "name": "delete_memory",
            "description": "Apaga uma memória específica pelo ID (obtido via list_memories). Use quando Ramon pedir para esquecer algo ou corrigir uma informação errada.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "fact_id": {"type": "integer", "description": "ID da memória a apagar."},
                },
                "required": ["fact_id"],
            },
        },
        {
            "name": "get_youtube_channel_stats",
            "description": (
                "Consulta estatísticas de um canal do YouTube: inscritos, views totais e número de vídeos. "
                "Use quando Ramon perguntar sobre o desempenho do canal, quantos inscritos tem, etc. "
                "O alias padrão do canal de Ramon é 'ramon'."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "channel_alias": {"type": "string", "description": "Alias do canal configurado. Ex: 'ramon'", "default": "ramon"},
                },
                "required": ["channel_alias"],
            },
        },
        {
            "name": "get_youtube_recent_videos",
            "description": (
                "Lista os vídeos mais recentes de um canal do YouTube com views, likes e links. "
                "Use quando Ramon perguntar sobre os últimos vídeos, desempenho de vídeos recentes, etc."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "channel_alias": {"type": "string", "description": "Alias do canal configurado. Ex: 'ramon'", "default": "ramon"},
                    "max_results": {"type": "integer", "description": "Número de vídeos a retornar (padrão: 5, máximo: 10).", "default": 5},
                },
                "required": ["channel_alias"],
            },
        },
        {
            "name": "get_facebook_page_stats",
            "description": (
                "Consulta estatísticas da página do Facebook de Ramon: curtidas, seguidores, descrição. "
                "Use quando Ramon perguntar sobre o desempenho da página, quantos seguidores tem no Facebook, etc."
            ),
            "input_schema": {"type": "object", "properties": {}, "required": []},
        },
        {
            "name": "get_instagram_profile",
            "description": (
                "Consulta o perfil do Instagram de Ramon: seguidores, seguindo, número de posts, bio. "
                "Use quando Ramon perguntar sobre o Instagram dele, quantos seguidores tem, etc."
            ),
            "input_schema": {"type": "object", "properties": {}, "required": []},
        },
        {
            "name": "get_instagram_recent_posts",
            "description": (
                "Lista as publicações recentes do Instagram de Ramon com curtidas, comentários e links. "
                "Use quando Ramon perguntar sobre os últimos posts, engajamento, métricas de publicações."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Número de posts a retornar (padrão: 5, máximo: 20).", "default": 5},
                },
                "required": [],
            },
        },
        {
            "name": "post_to_facebook",
            "description": (
                "Publica uma mensagem de texto na página do Facebook de Ramon. "
                "Use quando Ramon pedir para postar algo no Facebook ou publicar na página."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "Texto da publicação."},
                },
                "required": ["message"],
            },
        },
        {
            "name": "ixc_login",
            "description": (
                "Faz login no sistema IXC Soft da Servlink Telecom. "
                "Chame sem two_fa_code para iniciar. Se o IXC pedir 2FA, um código chega no e-mail "
                "ramon@servlink.com.br — então chame novamente passando o código. "
                "Use quando Ramon pedir acesso ao IXC, ONUs, rede neutra, ou sistema da Servlink."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "two_fa_code": {
                        "type": "string",
                        "description": "Código de 2 fatores recebido por e-mail. Deixe vazio para iniciar o login.",
                        "default": "",
                    },
                },
                "required": [],
            },
        },
        {
            "name": "ixc_get_onus_rede_neutra",
            "description": (
                "Lista as ONUs da rede neutra no IXC Soft da Servlink. "
                "Requer login prévio com ixc_login. "
                "Use quando Ramon perguntar sobre ONUs, clientes de rede neutra, ou fibra da Servlink."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Máximo de registros a retornar (padrão: 100).",
                        "default": 100,
                    },
                },
                "required": [],
            },
        },
        {
            "name": "ixc_get_onus_online_por_vlan",
            "description": (
                "Lista ONUs online da rede neutra agrupadas por VLAN no IXC Soft. "
                "Se vlan for fornecida, mostra apenas essa VLAN. "
                "Use quando Ramon perguntar quantas ONUs estão online por VLAN, ou clientes ativos por VLAN da rede neutra."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "vlan": {
                        "type": "string",
                        "description": "ID ou número da VLAN para filtrar. Vazio = agrupa todas as VLANs.",
                        "default": "",
                    },
                },
                "required": [],
            },
        },
        {
            "name": "ixc_screenshot",
            "description": (
                "Tira um screenshot da tela atual do IXC Soft para diagnóstico. "
                "Use quando quiser ver o estado atual da interface, verificar se login funcionou, "
                "ou entender a estrutura de uma página no IXC."
            ),
            "input_schema": {"type": "object", "properties": {}, "required": []},
        },
        {
            "name": "post_to_instagram",
            "description": (
                "Publica uma foto com legenda no Instagram de Ramon. "
                "A imagem deve ser uma URL pública acessível (JPEG/PNG). "
                "Use quando Ramon pedir para postar no Instagram com uma imagem e legenda."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "image_url": {"type": "string", "description": "URL pública da imagem (JPEG ou PNG). Deve ser acessível publicamente."},
                    "caption": {"type": "string", "description": "Legenda da publicação com hashtags. Opcional.", "default": ""},
                },
                "required": ["image_url"],
            },
        },
    ]


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
        elif tool_name == "create_reminder":
            return await tool_create_reminder(
                title=tool_input.get("title", ""),
                description=tool_input.get("description", ""),
                due_date=tool_input.get("due_date", ""),
            )
        elif tool_name == "list_reminders":
            return await tool_list_reminders(
                include_completed=tool_input.get("include_completed", False),
            )
        elif tool_name == "complete_reminder":
            return await tool_complete_reminder(
                reminder_id=int(tool_input.get("reminder_id", 0)),
            )
        elif tool_name == "take_screenshot":
            return await take_screenshot(
                url=tool_input.get("url", ""),
                full_page=tool_input.get("full_page", False),
            )
        elif tool_name == "browse_and_read":
            return await browse_and_read(url=tool_input.get("url", ""))
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
        elif tool_name == "save_memory":
            return await tool_save_memory(
                category=tool_input.get("category", "general"),
                fact=tool_input.get("fact", ""),
            )
        elif tool_name == "list_memories":
            return await tool_list_memories()
        elif tool_name == "delete_memory":
            return await tool_delete_memory(
                fact_id=int(tool_input.get("fact_id", 0)),
            )
        elif tool_name == "get_youtube_channel_stats":
            return await get_youtube_channel_stats(
                channel_alias=tool_input.get("channel_alias", "ramon"),
                api_key=config.YOUTUBE_API_KEY,
                channels_config=config.YOUTUBE_CHANNELS,
            )
        elif tool_name == "get_youtube_recent_videos":
            return await get_youtube_recent_videos(
                channel_alias=tool_input.get("channel_alias", "ramon"),
                api_key=config.YOUTUBE_API_KEY,
                channels_config=config.YOUTUBE_CHANNELS,
                max_results=tool_input.get("max_results", 5),
            )
        elif tool_name == "get_facebook_page_stats":
            return await get_facebook_page_stats(
                page_id=config.META_PAGE_ID,
                page_access_token=config.META_PAGE_ACCESS_TOKEN,
            )
        elif tool_name == "get_instagram_profile":
            return await get_instagram_profile(
                ig_user_id=config.META_IG_USER_ID,
                page_access_token=config.META_PAGE_ACCESS_TOKEN,
            )
        elif tool_name == "get_instagram_recent_posts":
            return await get_instagram_recent_posts(
                ig_user_id=config.META_IG_USER_ID,
                page_access_token=config.META_PAGE_ACCESS_TOKEN,
                limit=tool_input.get("limit", 5),
            )
        elif tool_name == "post_to_facebook":
            return await post_to_facebook(
                message=tool_input.get("message", ""),
                page_id=config.META_PAGE_ID,
                page_access_token=config.META_PAGE_ACCESS_TOKEN,
            )
        elif tool_name == "post_to_instagram":
            return await post_to_instagram(
                ig_user_id=config.META_IG_USER_ID,
                page_access_token=config.META_PAGE_ACCESS_TOKEN,
                image_url=tool_input.get("image_url", ""),
                caption=tool_input.get("caption", ""),
            )
        elif tool_name == "ixc_login":
            return await tool_ixc_login(
                ixc_email=config.IXC_EMAIL,
                ixc_password=config.IXC_PASSWORD,
                two_fa_code=tool_input.get("two_fa_code", ""),
            )
        elif tool_name == "ixc_get_onus_rede_neutra":
            return await tool_ixc_get_onus_rede_neutra(
                ixc_email=config.IXC_EMAIL,
                ixc_password=config.IXC_PASSWORD,
                limit=tool_input.get("limit", 100),
            )
        elif tool_name == "ixc_get_onus_online_por_vlan":
            return await tool_ixc_get_onus_online_por_vlan(
                ixc_email=config.IXC_EMAIL,
                ixc_password=config.IXC_PASSWORD,
                vlan=tool_input.get("vlan", ""),
            )
        elif tool_name == "ixc_screenshot":
            return await tool_ixc_screenshot(
                ixc_email=config.IXC_EMAIL,
                ixc_password=config.IXC_PASSWORD,
            )
        else:
            return f"Ferramenta desconhecida: '{tool_name}'."
    except Exception as exc:
        return f"Erro ao executar '{tool_name}': {exc}"
