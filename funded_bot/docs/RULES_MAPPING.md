# Funded Rules -> Config Mapping

- Max daily drawdown -> `account.max_daily_drawdown_pct`
- Max overall drawdown -> `account.max_overall_drawdown_pct`
- Max lot size -> `account.max_lot_size`
- Exposure limit -> `account.max_total_exposure_lots`
- News trading allowed? -> `news_filter.enabled` + block windows
- Weekend hold allowed? -> `weekend.hold_positions`
- Minimum trading days -> `account.min_trading_days`
- Consistency rule -> `account.consistency_profit_cap_pct`

## Enforcement Policy

- Rule break => `RuleViolation`
- Daily DD hit => new trades blocked
- Overall DD hit => `account.disabled = True`
- No exception mode by design
