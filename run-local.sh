#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
PARENT="$(dirname "$ROOT")"
PORT="${PORT:-4173}"
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 não encontrado. Instale Python 3 e tente novamente."
  exit 1
fi
echo "JALEP Mano local: http://127.0.0.1:${PORT}/$(basename "$ROOT")/"
echo "Para parar, pressione Ctrl+C."
python3 -m http.server "$PORT" --bind 127.0.0.1 --directory "$PARENT"
