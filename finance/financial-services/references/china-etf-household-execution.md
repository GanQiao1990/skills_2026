# China ETF household execution pattern

Use for household wealth-preservation / inflation-beating requests when the user wants concrete China-listed ETF implementation rather than abstract asset classes.

## When to use
- User has a finite RMB pool (for example 200k) and wants a durable family-fund style allocation.
- User explicitly wants China ETF implementation.
- Inputs are incomplete (age / liabilities / monthly surplus / max drawdown not fully known), so produce a conservative base-case decision memo instead of pretending to give regulated individualized advice.

## Recommended ETF roles
Prefer broad, function-first sleeves over narrow sector timing.

- Cash management / safety reserve: money-market ETF such as 511990
- Core equity beta: CSI 300 ETF such as 510300
- Defensive equity / dividend sleeve: dividend ETF such as 510880
- Bond stabilizer: government-bond ETF such as 511260 or similar treasury ETF
- Macro hedge: gold ETF such as 518880
- Optional satellite growth sleeve: small-cap broad ETF such as 512100, kept smaller than core sleeves

Do not let satellite / small-cap / thematic sleeves become the portfolio anchor for a family-fund style mandate.

## Public-data workflow
Use tools for all current facts.

1. Get current China ETF quotes from a live public endpoint such as Sina hq:
   - `https://hq.sinajs.cn/list=sh510300`
   - Parse name, previous close, current price, intraday high/low, amount, timestamp.
2. Get recent daily adjusted history from Tencent fqkline:
   - `https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sh510300,day,,,120,qfq`
   - Use `qfqday` when present, otherwise `day`.
3. Compute simple execution indicators from tools, not memory:
   - 20-day moving average
   - 60-day moving average
   - Drawdown from 60-day high
   - Position within 60-day range
   - Recent realized volatility (for example annualized from last 20 daily returns)
4. Convert indicators into staged-entry language:
   - `加速建仓`: meaningful pullback plus short-term weakness, usually suitable for defensive/hedge sleeves first
   - `正常建仓`: modest pullback / near moving averages
   - `只做底仓首笔/等待回撤`: strong trend near local highs; establish only a starter position
   - Bonds / cash sleeves can be funded more directly because their role is stability, not timing

## Practical rating rules used in this session
These are simple execution heuristics, not forecasts.

- If an equity/gold ETF is down meaningfully from its 60-day high and below the 20-day average, it can move into `加速建仓`.
- If it is modestly below the 20-day average or a few percent below the 60-day high, treat as `正常建仓`.
- If it is well above the 20-day / 60-day averages and sitting near the 60-day high, only open a starter position and wait for pullback rather than chasing.
- For treasury ETF sleeves, it is acceptable to allocate the main stabilizer sleeve without waiting for a deep pullback.

## Deliverable shape
When the user asks to "run the model" or "make the decision concrete", produce:

1. ETF role table
2. Current-data snapshot table with prices and computed indicators
3. Allocation table for the total RMB pool
4. First-tranche execution table showing how much to buy now vs hold in reserve
5. Second / third tranche trigger rules by ETF
6. Evaluation section: inflation-fighting role, drawdown control role, and governance / rebalancing rules

## Cautions
- Do not claim exact bottoms.
- Do not use narrow industry ETFs as the default family-fund implementation.
- Keep the memo explicit that this is a rule-based execution framework under incomplete household inputs.
- Preserve the repo’s safety posture: process, assumptions, and reviewability over certainty.
