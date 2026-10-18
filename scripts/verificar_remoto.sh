#!/usr/bin/env bash
# Verifica que la tarjeta A2A del segundo agente se pueda descargar.
# Uso: ./scripts/verificar_remoto.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$ROOT/agente-rodrigo/.venv/bin/python"

if [ ! -x "$PY" ]; then
  echo "No encuentro $PY. Crea primero el .venv de agente-rodrigo."
  exit 1
fi

"$PY" - "$ROOT" <<'PY'
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

root = Path(sys.argv[1])
load_dotenv(root / ".env")

url = (os.environ.get("A2A_URL_2") or "").rstrip("/")
assistant_id = (os.environ.get("A2A_ASSISTANT_ID_2") or "").strip()

if not url:
    raise SystemExit("Falta A2A_URL_2 en el .env de la raíz.")
if not assistant_id:
    raise SystemExit(
        "Falta A2A_ASSISTANT_ID_2 en el .env. En modo remoto el UUID es obligatorio."
    )

card_url = f"{url}/.well-known/agent-card.json?assistant_id={assistant_id}"
print("Consultando:", card_url)

try:
    with urllib.request.urlopen(card_url, timeout=30) as response:
        raw = response.read().decode("utf-8", "replace")
except urllib.error.HTTPError as exc:
    body = exc.read().decode("utf-8", "replace")
    if "1033" in body or "Cloudflare Tunnel error" in body:
        raise SystemExit(
            "Cloudflare error 1033: el túnel no está activo o cambió la URL. "
            "Pide la URL actual a tu compañero."
        )
    raise SystemExit(f"HTTP {exc.code} al pedir la tarjeta: {body[:300]}")
except Exception as exc:
    raise SystemExit(f"No se pudo conectar a {card_url}: {exc}")

try:
    card = json.loads(raw)
except json.JSONDecodeError:
    raise SystemExit(
        "La respuesta no es JSON. Probablemente el túnel devolvió una página de error "
        "de Cloudflare en lugar de la Agent Card."
    )

print("name:", card.get("name"))
print("description:", card.get("description"))
for interfaz in card.get("supportedInterfaces", []):
    print(
        "interface:",
        interfaz.get("protocolBinding"),
        interfaz.get("protocolVersion"),
        interfaz.get("url"),
    )
for skill in card.get("skills", []):
    print("skill:", skill.get("name"))
PY
