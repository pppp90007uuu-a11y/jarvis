# Deployment Checklist (VPS)

1. MT5 terminal install karo aur account login karo.
2. Python env setup:
   - `python -m venv .venv`
   - `pip install -r requirements.txt`
3. `config/funded_rules.json` me funded account exact rules fill karo.
4. Telegram token/chat id configure karo.
5. `tmux` ya `systemd` se `scripts/watchdog.sh` run karo.
6. Daily logs monitor karo:
   - `logs/bot.log`
   - `logs/error.log`

## Recommended Sequence

1. Backtest (1-2 years)
2. Walk-forward test
3. Demo funded simulation
4. Real funded deployment

## Hard KPIs

- Profit Factor > 1.2
- Rule violations = 0
- Max drawdown below configured caps
