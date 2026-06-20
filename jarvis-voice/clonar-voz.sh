#!/bin/bash
# ============================================================
# JARBAS — Script de Clonagem de Voz (ElevenLabs)
# Uso: bash clonar-voz.sh <arquivo-audio.mp3> <ELEVENLABS_API_KEY>
# ============================================================
# Envia o áudio para a API de clonagem do ElevenLabs e
# retorna o Voice ID para usar no .env do JARBAS.
# ============================================================

set -e

AUDIO_FILE="$1"
API_KEY="$2"
VOICE_NAME="${3:-JARBAS-JARVIS}"

# ── Validações ─────────────────────────────────────────────
if [[ -z "$AUDIO_FILE" || -z "$API_KEY" ]]; then
    echo ""
    echo "Uso: bash clonar-voz.sh <arquivo.mp3> <ELEVENLABS_API_KEY> [nome-da-voz]"
    echo ""
    echo "Exemplos:"
    echo "  bash clonar-voz.sh jarvis-samples.mp3 xxxxxxxx"
    echo "  bash clonar-voz.sh jarvis-samples.mp3 xxxxxxxx JARBAS-JARVIS"
    echo ""
    echo "Dicas para melhor resultado:"
    echo "  - Use áudio limpo, sem música de fundo ou ruído"
    echo "  - Mínimo 1 minuto de áudio (recomendado 3-5 min)"
    echo "  - Formato MP3 ou WAV, mono ou stereo"
    echo "  - Paul Bettany (JARVIS no Iron Man / Avengers)"
    echo ""
    exit 1
fi

if [[ ! -f "$AUDIO_FILE" ]]; then
    echo "Erro: arquivo '$AUDIO_FILE' não encontrado."
    exit 1
fi

FILE_SIZE=$(wc -c < "$AUDIO_FILE")
if [[ "$FILE_SIZE" -lt 50000 ]]; then
    echo "Aviso: arquivo muito pequeno (${FILE_SIZE} bytes)."
    echo "Para melhor qualidade de clonagem, use pelo menos 1 minuto de áudio."
    echo ""
fi

echo ""
echo "========================================"
echo "  JARBAS — Clonagem de Voz"
echo "========================================"
echo "  Arquivo:  $AUDIO_FILE"
echo "  Nome:     $VOICE_NAME"
echo "  Tamanho:  $(du -sh "$AUDIO_FILE" | cut -f1)"
echo "========================================"
echo ""
echo "Enviando para ElevenLabs..."
echo ""

# ── Chamada à API ──────────────────────────────────────────
RESPONSE=$(curl -s -w "\n%{http_code}" \
    -X POST "https://api.elevenlabs.io/v1/voices/add" \
    -H "xi-api-key: $API_KEY" \
    -F "name=$VOICE_NAME" \
    -F "description=Voz clonada do JARVIS (Paul Bettany) para o JARBAS" \
    -F "labels={\"use\": \"JARBAS\", \"language\": \"pt-BR\"}" \
    -F "files=@$AUDIO_FILE" \
)

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)

# ── Resultado ──────────────────────────────────────────────
if [[ "$HTTP_CODE" == "200" ]]; then
    VOICE_ID=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin)['voice_id'])" 2>/dev/null)

    if [[ -n "$VOICE_ID" ]]; then
        echo "========================================"
        echo "  SUCESSO! Voz clonada."
        echo "========================================"
        echo ""
        echo "  Voice ID: $VOICE_ID"
        echo ""
        echo "  Adicione ao .env do JARBAS:"
        echo "  ELEVENLABS_VOICE_ID=$VOICE_ID"
        echo ""
        echo "  Ou cole no painel Settings do JARBAS UI."
        echo "========================================"

        # Salva o Voice ID em um arquivo local
        echo "$VOICE_ID" > voice_id.txt
        echo "  (Voice ID salvo em: jarvis-voice/voice_id.txt)"
        echo ""
    else
        echo "Resposta inesperada da API:"
        echo "$BODY"
    fi

elif [[ "$HTTP_CODE" == "401" ]]; then
    echo "Erro 401: API key inválida."
    echo "Verifique ELEVENLABS_API_KEY."

elif [[ "$HTTP_CODE" == "422" ]]; then
    echo "Erro 422: Arquivo inválido ou parâmetros incorretos."
    echo "$BODY"

elif [[ "$HTTP_CODE" == "429" ]]; then
    echo "Erro 429: Limite de clonagens atingido no plano gratuito."
    echo "O plano Free permite 1 voz clonada. Delete a anterior no site."

else
    echo "Erro HTTP $HTTP_CODE:"
    echo "$BODY"
fi
