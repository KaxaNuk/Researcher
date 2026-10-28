---
source: https://www.wiley.com/en-us/Advanced+Portfolio+Management%3A+A+Quant%27s+Guide+for+Fundamental+Investors-p-9781119789796
citation: "Giuseppe A. Paleologo. John Wiley & Sons, 2021. ISBN 9781119789796. The date the link was last checked is not recorded."
local_copy: none
read: "2026-08-25; what was read: not recorded"
---

# Paleologo (2021) — *Advanced Portfolio Management: A Quant's Guide for Fundamental Investors*

> One section per chapter idea. Every section ends with what it means for **this** repository, as a
> blockquote. Where the book contradicts something we do, that is recorded as a contradiction rather
> than smoothed over.

The book is written for fundamental equity PMs who need the quant apparatus — risk models, sizing,
attribution — without becoming quants.

> Rewritten on 2026-10-27 for this copy, after FINDINGS_1.md reported on Sharadar.
>
> **Why this book matters more than the papers.** Most papers in
> [`BIBLIOGRAPHY.md`](../../BIBLIOGRAPHY.md) argue for or against a *signal*. This book supplies a
> **method for deciding whether the signal is doing anything**: sections 1, 5 and 6 below. It turns
> "the strategy beats its benchmark" into "this part of the return is the idea, and this part is
> beta, size and luck". Experiment 1 used it on claims 1 and 2. Its answer: three fifths of the
> holdings' compounded return is factor exposure, and once factors are stripped out the rule's
> selection is +6.7 points, against +22.3 for its control
> ([`FINDINGS_1.md`](../../../Experiments/Experiment_1/FINDINGS_1.md), *What attribution says*).

No copy of the book is kept here, so the table gives no pages. Which chapters were read was not
recorded: a chapter is *read* where a section below cites it, *skipped* otherwise.

| # | Chapter | Status | Claim | Note |
| --- | --- | --- | --- | --- |
| 1 | For Whom? Why? And How? | skipped | | |
| 2 | The Problem: From Ideas to Profit | skipped | | |
| 3 | A Tour of Risk and Performance | read | C1, C2 | [section 4](INDEX.md#4-alpha-estimates-are-far-noisier-than-beta-estimates) |
| 4 | An Introduction to Multi-Factor Models | skipped | | |
| 5 | Understand Factors | read | C1 | [sections 1 to 3](INDEX.md#1-momentum-is-relative-trend-following-is-absolute) |
| 6 | Use Effective Heuristics for Alpha Sizing | read | C2 | [sections 6 and 7](INDEX.md#6-size-by-risk-adjusted-alpha) |
| 7 | Manage Factor Risk | skipped | | |
| 8 | Understand Your Performance | read | C1, C2, C3 | [sections 5, 9 and 10](INDEX.md#5-decompose-pl-into-factor-and-idiosyncratic--then-decompose-the-idiosyncratic-part) |
| 9 | Manage Your Losses | read | C1 | [section 8](INDEX.md#8-stop-losses-the-real-cost-is-forgone-profit-not-commission) |
| 10 | Set Your Leverage Ratio for a Sustainable Business | skipped | | |
| 11 | Appendix | skipped | | |

---

## 1. Momentum is relative; trend-following is absolute

*(section 5.2.3)*

The book draws a distinction that most practitioner writing blurs. **Momentum is relative**: it
ranks a stock against its peers and goes long the winners, short the losers, so a momentum book is
roughly cross-sectional and roughly dollar-neutral. **Trend-following is absolute**: it holds
whatever is going up, sized by how much it is going up, with no reference to anyone else. In the
book's own toy example the same six technology names produce a long-everything trend portfolio and
a long-two / short-two momentum portfolio.

> Rewritten on 2026-10-27 for this copy, after FINDINGS_1.md reported on Sharadar.
>
> **What this implies for Golden Flow: claim 1 is a trend claim, and the book still carries
> momentum.** The golden cross asks whether *this* name is above its own average, never whether it
> out-trends its peers. The factor model's momentum factor measures the relative kind, so the
> blueprint's lead 8 expected it to see little. It saw +90.5 points compounded, the largest style,
> against 539.8 from the market; the control, without the cross, reads +75.9
> ([`FINDINGS_1.md`](../../../Experiments/Experiment_1/FINDINGS_1.md), the factor model). Ranking by
> traded value buys recent winners; the cross adds only a little momentum of its own.

## 2. Momentum has a term structure

*(section 5.2.3, citing Novy-Marx 2012)*

Past performance predicts future returns with a sign that flips twice as the lookback lengthens:
the most recent month **reverses** (last month's winners underperform, and more strongly the shorter
the window), one month to one year **continues** (this is the real momentum effect), and beyond a
year **reverses** again.

> Rewritten on 2026-10-27 for this copy, after FINDINGS_1.md reported on Sharadar.
>
> **What this implies for Golden Flow: nothing measured here.** Golden Flow computes no return over
> a fixed lookback as a feature. Its signal is the 50/200 cross, read as a state, which this section
> does not test. It stays as context for claim 1, and as a warning for any later feature built on
> last month's return: the book expects that sign to be negative.

## 3. Momentum's return is partly compensation for a fat left tail

*(section 5.2.3)*

The book z-scores daily momentum factor returns by trailing three-month volatility and shows the
quantiles are materially worse than Gaussian in the left tail. Alongside the behavioural stories
(under-reaction, over-reaction, "frogs in the pan"), it presents the risk-based reading: the premium
is paid for bearing crash risk, and the crash is real.

> Rewritten on 2026-10-27 for this copy, after FINDINGS_1.md reported on Sharadar.
>
> **What this implies for Golden Flow: its tail is worse than the market's.** Golden Flow is long
> only, so it holds none of the short leg that owns this tail. Its worst drawdown is still −82.6%,
> against −53.9% for the KN US Equity Core and −91.7% for the control, the same rule without the
> cross ([`FINDINGS_1.md`](../../../Experiments/Experiment_1/FINDINGS_1.md)). A book of the most
> traded names holds whatever the market is crowding into, and in 2000 that was the bubble. Mean and
> variance are not enough to judge it, so the findings report the drawdown and each sub-period
> beside the Sharpe.

## 4. Alpha estimates are far noisier than beta estimates

*(section 3.3)*

Regressing a single stock's returns on the market gives a beta with a tight confidence interval and
an alpha whose interval is wider than the estimate itself — the book's worked example has an alpha
point estimate whose 95% band spans both large negative and positive values, while beta lands inside
a narrow range. Alphas also move a lot year to year; betas do not.

> Rewritten on 2026-10-27 for this copy, after FINDINGS_1.md reported on Sharadar.
>
> **What this implies for Golden Flow: its alpha has no error bar.** The engine puts the rule's
> alpha against the index at −1.91%, −0.40% at the flat row, and the control's at −3.21%, with no
> interval around any of them ([`FINDINGS_1.md`](../../../Experiments/Experiment_1/FINDINGS_1.md)).
> What is estimated precisely is the exposure: 400.4 of the holdings' 685.4 points of compounded
> return are factors. The part claims 1 and 2 lean on is thin: once factors are stripped out, the
> rule's selection is +6.7 points over 26 years. One window cannot make that a stable property of
> the strategy.

## 5. Decompose P&L into factor and idiosyncratic — then decompose the idiosyncratic part

*(section 8.1–8.2, takeaways section 8.6)*

The recommended order is: split P&L into factor and idiosyncratic; if the factor part is large, your
factor risk is large and should be reduced by hedging, optimisation or tactical trading. Then split
the **idiosyncratic** part three ways:

- **Selection** — being directionally right about which names to hold.
- **Sizing** — being right about *how much*, so the big positions are the good ones.
- **Timing** — carrying risk when your views are better than average.

The mechanism is **counterfactual portfolios rather than a formula.** To measure sizing skill,
rewrite history with every position **equalised within each date**, keeping the side and the total
gross value unchanged, then compare the Sharpe of that book with the real one. The difference is
what sizing contributed. The book also warns to drop economically insignificant positions first, or
the analysis is dominated by residual slivers nobody was really betting on.

> Rewritten on 2026-10-27 for this copy, after FINDINGS_1.md reported on Sharadar.
>
> **What this implies for Golden Flow: Experiment 1 ran two of the three legs.** Sizing is the
> equal-weight arm: the rule's own names on its own dates, equalised. It earns a Sharpe of 0.157
> against the rule's 0.221 at the flat row, and an idiosyncratic return of +87.8 points against
> +285.0. That is claim 2's evidence. Selection is the twenty random books, drawn from the members
> the control may hold on the rule's dates: their idiosyncratic return runs from −57.7 to +679.8,
> and the rule beats 15 of the 19 priced whole, short of the 16 of 20 the blueprint asked. Timing
> was not priced: the shifted-entry arm was not run
> ([`FINDINGS_1.md`](../../../Experiments/Experiment_1/FINDINGS_1.md)). The book's advice to drop
> slivers first is built into claim 3: the 1% floor holds no name smaller than that.

## 6. Size by risk-adjusted alpha

*(section 6.3–6.5, takeaways section 6.8)*

The book's sizing recipe: form a view of expected **idiosyncratic** return per name, put all views on
one horizon, neutralise them against factor loadings, then convert to position sizes by either a
proportional rule (position proportional to standardised alpha) or a shrunk mean-variance rule. It
notes the simplest proportional rule is often preferable in practice, especially in sector-focused
books.

> Rewritten on 2026-10-27 for this copy, after FINDINGS_1.md reported on Sharadar.
>
> **What this implies for Golden Flow: a contradiction, kept visible.** Golden Flow sizes by traded
> value. That is a capacity and attention argument, not a forecast of idiosyncratic return, so under
> the book's framework it is a constraint used as a weighting scheme. Claim 2 still won as a book: a
> Sharpe of 0.162 against 0.087 for the same names equally weighted. Attribution says how: the
> idiosyncratic return is +285.0 points for the rule against +87.8 for equal weight, and the
> residual selection +6.7 against −19.0
> ([`FINDINGS_1.md`](../../../Experiments/Experiment_1/FINDINGS_1.md)). The book would still ask for
> a forecast behind the weights, and no note in this folder supplies one.

## 7. Volatility targeting is the cheap drawdown lever

*(section 6.6, takeaway section 6.8 #6)*

Scale portfolio gross exposure over time so that **predicted idiosyncratic dollar volatility** hits a
constant target. The book states plainly that volatility targeting improves risk-adjusted
performance.

> Rewritten on 2026-10-27 for this copy, after FINDINGS_1.md reported on Sharadar.
>
> **What this implies for Golden Flow: an untested lever, by design.** The rule has no risk model:
> each screen left out is a lever a later experiment has to earn
> ([`BLUEPRINT_1.md`](../../../Experiments/Experiment_1/BLUEPRINT_1.md), *Rules*). The golden cross
> already lowers volatility: 25.73% against 29.52% for the control. A volatility target would be
> tested against this rule in a new experiment, never added to it.

## 8. Stop-losses: the real cost is forgone profit, not commission

*(chapter 9, takeaways section 9.4)*

The book treats stop-loss policies as necessary — as a put against the option-like payoff a PM
holds, and as tail insurance — while being clear about the two costs: transaction costs from
de-grossing and re-grossing, and **performance degradation from profits given up**. Its conclusion
is that the second dominates the first. It also finds the difference between single-threshold and
two-threshold rules to be small, which is a useful licence not to over-engineer the rule.

> Rewritten on 2026-10-27 for this copy, after FINDINGS_1.md reported on Sharadar.
>
> **What this implies for Golden Flow: claim 1 pays this cost, and the findings show where.** The
> golden cross is the rule's exit; it runs no stop-loss besides. Its benefit is the drawdown:
> −82.6% against −91.7% for the control. Its cost is forgone profit: in 2009–2017 the names it kept
> out rose faster, and the control won that sub-period, 15.88% a year against 11.80%
> ([`FINDINGS_1.md`](../../../Experiments/Experiment_1/FINDINGS_1.md), prediction 1). Neither side
> was tuned: the 50/200 pair is the most widely known one, taken as it is.

## 9. Execution: match position building to the alpha's horizon

*(section 8.3, takeaway section 8.6 #8)*

Build positions consistently with how long the alpha is expected to last; VWAP is called out as a
good heuristic; and the book's blunt aside is that most readers' participation rate is higher than it
ought to be.

> Rewritten on 2026-10-27 for this copy, after FINDINGS_1.md reported on Sharadar.
>
> **What this implies for Golden Flow: the orders are few; participation is a bound.** Golden Flow
> trades once a month at the next open, about twenty orders on each date, and a band leaves a held
> name alone when its target moved by half a point or less. Participation is stated, not modelled.
> At 1% of a name's 63-day traded value, the rule's own score, the worst trade allows a $25.9
> million book, the 1st percentile $69.6 million and the median $3.25 billion
> ([`FINDINGS_1.md`](../../../Experiments/Experiment_1/FINDINGS_1.md)). Golden Flow's turnover is
> 2.16 times its value a year, one way. Market impact is modelled only as far as the engine's
> slippage does, and that model read a megacap's daily range as spread.

## 10. Diversify as much as you can — but not more than that

*(section 8.2.2, takeaway section 8.6 #9)*

Diversification improves the Sharpe of a book with genuine skill, but the marginal benefit decays,
and past some point extra names dilute the edge without materially reducing risk.

> Rewritten on 2026-10-27 for this copy, after FINDINGS_1.md reported on Sharadar.
>
> **What this implies for Golden Flow: claim 3's bounds answer it, not a count.** No count is
> chosen. The 20% cap and the 1% floor hold a median of 43 names on a rebalance date, 19 to 58,
> behaving like 24.1 effective positions
> ([`FINDINGS_1.md`](../../../Experiments/Experiment_1/FINDINGS_1.md)). The sweep moves the floor: a
> Sharpe of 0.242 at 0.5%, 0.221 at 1% and 0.233 at 2%, at the flat row, each ahead of its own
> control. The floor stays at the owner's 1%: a floor picked from this sweep would be chosen on the
> metric it is judged by.

---

## Distilled into Golden Flow's language

> Rewritten on 2026-10-27 for this copy, after FINDINGS_1.md reported on Sharadar.
>
> Each idea of the book, and what it implies for claims 1 to 3:
>
> - **Momentum (relative) is not trend-following (absolute).** Claim 1 is a trend claim; the factor
>   model still sees +90.5 points of momentum, the largest style, from the ranking more than the
>   cross.
> - **Momentum's term structure: 1m reverses, 12-1 continues, beyond 12m reverses.** No claim:
>   Golden Flow computes no return over a lookback.
> - **Momentum's premium is partly tail-risk compensation.** Long only, no short leg, and still a
>   worst drawdown of −82.6% against the Core's −53.9%.
> - **Alpha estimates are noisy, betas are not.** No error bar on the alpha; the residual selection
>   is +6.7 points over 26 years.
> - **Selection, sizing and timing, by counterfactual books.** Run for claims 1 and 2. Sizing: 0.221
>   against 0.157 equally weighted. Selection: 15 of 19 random books beaten, short of the bar.
>   Timing: not run.
> - **Size by risk-adjusted alpha.** Claim 2 sizes by traded value instead: a contradiction kept
>   visible.
> - **Volatility targeting improves risk-adjusted return.** An untested lever, for a later
>   experiment against this rule.
> - **A stop-loss costs forgone profit, not commission.** Claim 1's cost: the control won 2009–2017.
> - **Execution matched to the alpha's horizon; watch the participation rate.** Monthly at the open
>   with a band; capacity stated as a participation bound, not modelled.
> - **Diversify, but not past the point of dilution.** Claim 3's bounds set the count: a median of
>   43 names, 24.1 effective.

## What this book does not settle for us

> Rewritten on 2026-10-27 for this copy, after FINDINGS_1.md reported on Sharadar.
>
> - It assumes a **factor risk model is available** and mostly discusses what to do with one. We
>   have the KN US Equity Factor Model through the attribution stage but not inside portfolio
>   construction, so chapter 7, *Manage Factor Risk*, and the quantitative appendix, chapter 11,
>   are currently unreachable machinery.
> - It is written for **long/short, factor-neutral, market-neutral** books. Golden Flow is long-only
>   and deliberately carries beta. Several recommendations — factor neutralisation before sizing
>   above all — would change the strategy into a different one rather than improve it.
> - It says nothing about **universe construction or survivorship**, which is step 2 here. For that,
>   see [`BIBLIOGRAPHY.md`](../../BIBLIOGRAPHY.md) Part 5.
> - It says nothing about **multiple testing or Sharpe deflation**, which is still open here: the
>   deflated Sharpe of the rule against its 152 trials is not computed. For that, see Part 5 as
>   well.
