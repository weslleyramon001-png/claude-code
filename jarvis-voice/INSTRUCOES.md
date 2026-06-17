# Como Clonar a Voz do JARVIS para o JARBAS

> Guia passo a passo para quando Ramon chegar em casa

---

## O que você vai precisar

- [ ] Conta ElevenLabs com API Key (você já tem)
- [ ] Arquivo de áudio do JARVIS (Paul Bettany) — limpo, sem música
- [ ] ~5 minutos

---

## Passo 1 — Baixar o áudio do JARVIS

### Opção A — cobalt.tools (mais fácil, sem instalar nada)

1. Abra **cobalt.tools** no navegador
2. Cole a URL do YouTube
3. Selecione "Audio only" → Download
4. Salve como `jarvis-raw.mp3`

### Opção B — yt-dlp (linha de comando)

```bash
# Instalar yt-dlp
pip install yt-dlp

# Baixar só o áudio
yt-dlp -x --audio-format mp3 -o "jarvis-raw.%(ext)s" "URL_DO_VIDEO"
```

### Vídeos recomendados para buscar no YouTube

Busque por:
- `"JARVIS all scenes Iron Man"` — compilação de cenas
- `"JARVIS voice compilation no music"` — sem música de fundo
- `"Paul Bettany JARVIS clean audio"` — áudio limpo

> **Importante:** Escolha vídeos SEM música de fundo.
> O JARVIS geralmente fala limpo nas cenas de laboratório/HUD.

---

## Passo 2 — Limpar o áudio (opcional, mas recomendado)

Se o áudio tiver algum ruído de fundo, use o **ElevenLabs Voice Isolation**:

1. Acesse **elevenlabs.io → Tools → Voice Isolation**
2. Faça upload do `jarvis-raw.mp3`
3. Baixe a versão limpa

Ou use o **Adobe Podcast** (gratuito, online):
1. **podcast.adobe.com/enhance**
2. Upload → Enhance → Download

---

## Passo 3 — Clonar a voz no ElevenLabs

### Via Site (mais fácil)

1. Acesse **elevenlabs.io**
2. Clique em **Voices** → **Add a new voice**
3. Selecione **"Instant Voice Cloning"**
4. Upload do arquivo de áudio
5. Dê o nome: `JARBAS-JARVIS`
6. Clique em **Add Voice**
7. Copie o **Voice ID** gerado

### Via Script (automatizado)

```bash
cd /home/user/claude-code/jarvis-voice

# Execute o script de clonagem
bash clonar-voz.sh jarvis-limpo.mp3 SUA_ELEVENLABS_API_KEY
```

O script vai exibir o **Voice ID** e salvar em `voice_id.txt`.

---

## Passo 4 — Configurar no JARBAS

Depois de clonar, você tem o Voice ID. Coloque ele no `.env`:

```
ELEVENLABS_VOICE_ID=id_gerado_aqui
```

Ou cole diretamente no painel **Settings** do JARBAS UI.

---

## Dicas de qualidade

| Recomendado | Evitar |
|------------|--------|
| 3-5 minutos de áudio | Menos de 30 segundos |
| Voz clara, sem eco | Áudio com reverb ou eco |
| Sem música de fundo | Trilha sonora misturada |
| Volume consistente | Volume flutuante |
| Arquivo único | Vários arquivos curtos |

---

## Vozes PT-BR de backup (já disponíveis no ElevenLabs)

Se a clonagem não funcionar bem, estas vozes nativas PT-BR são excelentes:

| Nome | ID | Perfil |
|------|----|--------|
| Mateus | `XrExE9yKIg1WjnnlVkGX` | Masculino, claro, profissional |
| Daniel | `onwK4e9ZLuTAKqWW03F9` | Masculino, grave, autoritário |
| Adam | `pNInz6obpgDQGcFmaJgB` | Inglês, padrão ElevenLabs |
