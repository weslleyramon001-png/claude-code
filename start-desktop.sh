#!/bin/bash
# start-desktop.sh — Inicia display virtual para Claude controlar apps graficamente
# Executado automaticamente no início de cada sessão

pkill Xvfb 2>/dev/null || true
Xvfb :99 -screen 0 1280x800x24 -ac &
export DISPLAY=:99
echo "export DISPLAY=:99" >> ~/.bashrc
echo "✅ Display virtual :99 ativo (1280x800)"
