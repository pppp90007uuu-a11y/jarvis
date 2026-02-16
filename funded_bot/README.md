# Funded Account MT5 Bot Starter (Hindi)

Yeh project aapke diye hue 6 points ko **ek integrated starter framework** me convert karta hai:

- Funded account hard rules (no-exception rejection)
- Strategy + Risk engine + Session/News filters
- Backtest -> forward -> demo rollout workflow
- VPS deployment helpers + auto-restart + alerts

## Quick Start

```bash
cd funded_bot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.main --config config/funded_rules.json --mode dry-run
```

## Architecture

- `src/strategy.py` -> EMA trend + pullback confirmation + ATR SL + RR TP
- `src/risk_engine.py` -> daily/overall DD, spread, slippage, news/session, exposure checks
- `src/executor.py` -> execution abstraction (MT5 bridge ready)
- `src/main.py` -> bot orchestration loop
- `config/funded_rules.json` -> prop-firm style hard limits

## IMPORTANT

- Real execution ke liye `MetaTrader5` terminal setup aur broker symbols mapping required hai.
- Is starter ko funded challenge pe live deploy karne se pehle `backtest + forward + demo simulation` mandatory run karo.
