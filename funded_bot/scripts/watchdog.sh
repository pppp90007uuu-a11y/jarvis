#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

while true; do
  ./scripts/run_bot.sh >> logs/bot.log 2>> logs/error.log || true
  sleep 60
done
