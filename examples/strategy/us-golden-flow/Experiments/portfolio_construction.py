"""
Portfolio construction -- step 4 of 8, the second shared module.  Turns the set of securities a
rule calls eligible into the weights a book holds, calling the KaxaNuk Portfolio Construction
library where it is installed.

In plain words: how much of what, and how often you change your mind.

Runs inside an experiment notebook, from the rule in section 2, on the matrices the securities
panel built.

What is expected here is one function signature and a few things behind it:

- The signature.  Given the securities eligible today, a returns history that has already been
  cut off before today and, for a scheme that sizes by a feature, that feature as it stood before
  today, return one weight per security, summing to at most 1.0.  Every weighting scheme -- equal
  weight, proportional to a score, or any sizing method the library registers whose configuration
  has no required field: inverse volatility, risk parity, hierarchical risk parity -- is the same
  shape, so swapping one for another is one line in the rule cell and nothing else in the notebook
  moves.  That is what makes two experiments comparable rather than merely adjacent.
- The library inside the signature, never around it.  Build one of its methods per rebalance date,
  on the history already cut: a method that estimates from returns uses whatever history it was
  built with, and the library's own pipeline builds each method once for every date.  Import it
  inside a guard -- it is KaxaNuk's own library, installed by hand -- and stop with an error that
  names a method needing it when it is absent.  Equal weight needs nothing.
- At most one, not exactly one.  A strategy that can go to cash cannot satisfy the stricter form;
  what the weights leave is cash, which the engine holds and pays interest on.
- The constraints every scheme respects, as arguments of `build_weights`: a maximum weight and a
  minimum holding count.  One the blueprint does not name is switched off, and a lever a later
  experiment has to earn by beating the book without it.  Bounds the blueprint names -- a cap and a
  floor on each weight -- are the design, not levers to earn: the blueprint says whether a capped
  name's excess goes to cash or to the other names, and the control holds the same bounds.
- The timing helpers that cannot be forgotten if they live here: lag the eligibility so the set
  used on rebalance date t is the one observed at t-1; rebalance on a calendar -- the first trading
  day of each month, decided on the close before it -- or only on the dates that set changes; and a
  no-trade band, so a held name whose target barely moved is left as it drifted.  A weight that has
  not moved is not a reason to pay commission, nor an order anyone wants to place by hand.  The
  band is decided at the close and written at the next open, and what the kept names hold over
  their targets comes out of the traded names, so the book never exceeds one.
- No day of hindsight for a delisting.  The engine sells a position whose prices stop at its last
  price.  A gap inside a series, which the engine cannot price, is a blocking row of
  `Universe/Data_Issues.csv`, and the name is excluded by name from every book rather than traded
  around, so no book ever trades off its own dates.
- Causality by construction.  A weigher never sees a date, only a history -- and a score, where
  the scheme sizes by one -- already cut off before the date it sizes, so it cannot reach into the
  future even by accident.  The module makes that cut once, for the book and its control alike.

It produces the `REBALANCE_DATES x securities` target weights the rule cell hands to the
diagnostics and the weight file, and, under a band, the weights actually struck.

It prevents a good signal in a portfolio nobody could hold -- and a weighting difference that reads
as a signal difference because each notebook invented its own sizing.
"""

# --- example: begin ---

import importlib.util

import numpy
import pandas

__all__ = [
    "LIBRARY_INSTALLED",
    "banded_book",
    "bounded_book",
    "bounded_by_score",
    "build_weights",
    "exit_before_price_stops",
    "first_trading_days_of_month",
    "lag_eligibility",
    "rebalance_dates_on_change",
    "select_rebalance_dates",
    "weigh",
]

# KaxaNuk's own library, installed by hand rather than by `uv sync`.  Equal weight needs nothing,
# so the module stays usable without it and says so instead of failing on import.
LIBRARY_INSTALLED = importlib.util.find_spec("kaxanuk.portfolio_construction") is not None


def banded_book(
    targets: "pandas.DataFrame",
    decision_prices: "pandas.DataFrame",
    fill_prices: "pandas.DataFrame",
    band: float,
) -> "pandas.DataFrame":
    """
    The book actually struck on each rebalance date: the target, except where a trade is too small.

    A name held since the last rebalance and still in the target keeps the weight it drifted to
    when its target differs from that weight by no more than `band`; every other name -- an entry,
    an exit, a held name whose target moved further -- takes its target.  The decision is made on
    `decision_prices`, the close before the fill, so it uses nothing the person placing the orders
    could not see; the kept weight is then written as it stands at `fill_prices`, the fill, which is
    how "leave this name alone" is said in a weight file.  What the kept names hold over their
    targets comes out of the traded names in proportion, so the book never exceeds one; what they
    hold under it is left in cash.  Cash is carried flat between rebalances: its interest is the
    engine's, and a few basis points of it moves no decision.
    """
    dates = list(targets.index)
    struck_rows = {
        dates[0]: targets.loc[dates[0]],
    }

    for previous_date, date in zip(
        dates[:-1],
        dates[1:],
        strict=True,
    ):
        target = targets.loc[date]
        previous_weights = struck_rows[previous_date]
        decided = _drifted(
            previous_weights,
            decision_prices.loc[previous_date],
            decision_prices.loc[date],
        )
        at_fill = _drifted(
            previous_weights,
            fill_prices.loc[previous_date],
            fill_prices.loc[date],
        )
        held_both = (previous_weights > 0) & (target > 0)
        small = (target - decided).abs() <= band
        kept = held_both & small & at_fill.notna()
        kept_total = float(at_fill[kept].sum())
        traded_total = float(target[~kept].sum())
        room = 1.0 - kept_total
        scale = min(1.0, room / traded_total) if traded_total > 0 else 1.0
        traded = target.where(~kept, 0.0) * scale
        struck = traded.where(~kept, at_fill)
        struck_rows[date] = struck.fillna(0.0)

    return pandas.DataFrame.from_dict(
        struck_rows,
        orient="index",
    )


def bounded_book(
    eligibility: "pandas.DataFrame",
    scores: "pandas.DataFrame",
    maximum_weight: float,
    minimum_weight: float,
) -> "pandas.DataFrame":
    """
    The target book on every date: the eligible names by score, the bounds setting how many.

    The score is cut here, once, to the value it had at the close before each date -- the matrix
    is moved one row down its own calendar, which is the panel's trading calendar -- so no notebook
    writes a `.shift(1)` of its own.  Each date is then sized by `bounded_by_score`.  The book on
    every date, not only on rebalance dates, is what lets a rule re-strike exactly when the held set
    changes.
    """
    scores_before = scores.shift(1)
    rows = {}

    for date in eligibility.index:
        eligible = eligibility.loc[date]
        names = eligible.index[eligible.to_numpy(dtype=bool)]
        score = scores_before.loc[date, names]
        rows[date] = bounded_by_score(
            score,
            maximum_weight,
            minimum_weight,
        )

    book = pandas.DataFrame.from_dict(
        rows,
        orient="index",
    )
    aligned = book.reindex(
        index=eligibility.index,
        columns=eligibility.columns,
    )

    return aligned.fillna(0.0)


def bounded_by_score(
    score: "pandas.Series",
    maximum_weight: float,
    minimum_weight: float,
) -> "pandas.Series":
    """
    Size one date's eligible names in proportion to their score, inside a cap and a floor.

    Names are taken in order of score, highest first.  For a given count, each weight is its score
    over the sum of the counted names' scores, capped at `maximum_weight`, the excess spread over
    the uncapped names in proportion until no name is above the cap.  The count grows while the
    smallest weight stays at or above `minimum_weight`; the last count that passed is the book.
    As the count grows the proportional share of every uncapped name can only fall, so the first
    count to fail ends the walk.  With too few names for the cap to place every dollar, each takes
    the cap and the rest is left uninvested: the weights sum to at most one.  A name with no score,
    or a score that is not positive, is not counted.  Ties are broken by name, so the book never
    depends on the order the columns arrived in.
    """
    usable = score[score > 0].dropna()
    by_name = usable.sort_index()
    ordered = by_name.sort_values(
        ascending=False,
        kind="mergesort",
    )
    values = ordered.to_numpy(dtype=float)
    counts = range(1, len(values) + 1)
    first_failing = next(
        (
            count
            for count in counts
            if _capped_proportional(values[:count], maximum_weight).min() < minimum_weight
        ),
        None,
    )
    held_count = len(values) if first_failing is None else first_failing - 1
    weights = _capped_proportional(
        values[:held_count],
        maximum_weight,
    )

    return pandas.Series(
        weights,
        index=ordered.index[:held_count],
        dtype=float,
    )


def build_weights(
    eligibility: "pandas.DataFrame",
    returns: "pandas.DataFrame",
    rebalance_dates: "pandas.DatetimeIndex",
    method: str,
    maximum_weight: float | None,
    minimum_holdings: int,
    scores: "pandas.DataFrame | None" = None,
) -> "pandas.DataFrame":
    """
    Build the target book on each rebalance date, one weigher call per date.

    The history handed to the weigher is cut off strictly before the date it is sizing, so a method
    that estimates anything from returns cannot reach into the future even by accident; the score
    a feature-sized method reads is cut the same way, in the same place, and is the last row
    strictly before the date.  A date with fewer eligible securities than the minimum holds nothing
    at all: a book of four names is not a small version of a book of thirty, it is a different bet.
    """
    rows = {}

    for date in rebalance_dates:
        eligible = eligibility.loc[date]
        selected = tuple(eligible[eligible].index)

        if len(selected) < minimum_holdings:
            rows[date] = pandas.Series(
                0.0,
                index=eligibility.columns,
            )

            continue

        history = returns.loc[returns.index < date, list(selected)]
        scores_before = None if scores is None else scores.loc[scores.index < date]
        has_score = scores_before is not None and len(scores_before) > 0
        score = scores_before.iloc[-1] if has_score else None
        sized = weigh(
            selected,
            history,
            method,
            maximum_weight,
            score,
        )
        aligned = sized.reindex(eligibility.columns)
        rows[date] = aligned.fillna(0.0)

    return pandas.DataFrame(rows).transpose()


def exit_before_price_stops(
    tradable: "pandas.DataFrame",
) -> "pandas.DataFrame":
    """
    Tradable on a day and on the next one: a name whose prices stop tomorrow is sold today.

    When a company is delisted, or a corporate event leaves its price series with a gap, the engine
    cannot trade it on a day it has no price -- and a book that still holds it on that day cannot be
    re-struck at all.  So the book re-strikes on the last day the name is priced, t-1, and sells it
    there, at a real price.  The day the prices stop is known only the day after, so this is one day
    of hindsight: the leak `AGENTS.md` names for a delisting exit, applied to every stop in a price
    series.  The last day of the matrix has no next day to look at, and is taken as tradable, so a
    window's end never empties the book.
    """
    tomorrow = tradable.shift(
        -1,
        fill_value=True,
    )

    return tradable & tomorrow.astype(bool)


def first_trading_days_of_month(
    calendar: "pandas.DatetimeIndex",
) -> "pandas.DatetimeIndex":
    """
    The first trading day of every month in the calendar, the first day of the calendar included.

    A monthly book is decided on the month's last close and filled at the next open, so it is dated
    on the first trading day of the next month: the weight file's date is the day the orders go in,
    and everything the rule reads on that date was known at the close before it.
    """
    months = calendar.to_period("M")
    starts = months != numpy.roll(months, 1)
    starts[0] = True

    return calendar[starts]


def lag_eligibility(
    eligibility: "pandas.DataFrame",
) -> "pandas.DataFrame":
    """
    Shift the eligible set by one day, so a book struck on date t uses what was known at t-1.

    This is the one causal cut in the whole pipeline, and it lives here because a rule cell that
    has to remember it is a rule cell that will one day forget.
    """

    shifted = eligibility.shift(
        1,
        fill_value=False,
    )

    return shifted.astype(bool)


def rebalance_dates_on_change(
    eligibility: "pandas.DataFrame",
) -> "pandas.DatetimeIndex":
    """
    Keep only the dates on which the target set differs from the one before it.

    The event-driven rule: the first day anything is held counts as a change, because going from
    holding nothing to holding something is a trade, and between changes the book drifts and nothing
    is done.  A calendar rebalance on an unchanged set is pure cost.
    """
    previous = eligibility.shift(
        1,
        fill_value=False,
    )
    changed = eligibility.ne(previous).any(axis=1)

    return eligibility.index[changed.to_numpy()]


def select_rebalance_dates(
    eligibility: "pandas.DataFrame",
    band: float,
    held: "pandas.DataFrame | None" = None,
) -> "pandas.DatetimeIndex":
    """
    Keep only the dates on which the target set has moved far enough from the one before it.

    Distance is the share of the book a move would trade: with equal weights, three names out of
    thirty is ten percent.  A signal that has not moved is not a reason to pay commission, which is
    what the band is for; `held` is accepted so a later experiment can measure drift against the
    book actually held rather than against the previous target.
    """
    reference = eligibility if held is None else held
    previous = reference.shift(1)
    changed = (reference != previous).sum(axis=1)
    holdings = reference.sum(axis=1)
    # A date holding nothing has no book to measure a move against, so it always counts as a move:
    # dividing by it would be a zero denominator, and treating it as "nothing changed" would leave
    # the book stuck out of the market.
    measurable = holdings.where(holdings > 0)
    turnover = (changed / measurable).fillna(1.0)
    triggered = turnover >= band
    triggered.iloc[0] = True

    return eligibility.index[triggered]


def weigh(
    selected: tuple[str, ...],
    history: "pandas.DataFrame",
    method: str,
    maximum_weight: float | None,
    score: "pandas.Series | None" = None,
) -> "pandas.Series":
    """
    Size one date's eligible set, by the named method, on the history and the score already cut.

    Equal weight is computed here because it needs nothing but the set, and proportional-to-score
    because it needs nothing but the score -- a security with no usable score, null or not
    positive, is dropped rather than guessed at and the rest renormalised over what remains.  Every
    other method is the library's, built fresh for this date.  A cap is applied by trimming and
    leaving the excess in cash rather than redistributing it, so a cap can never quietly
    concentrate the book further.
    """
    if method == "equal_weight":
        weights = pandas.Series(
            1.0 / len(selected),
            index=list(selected),
        )
    elif method == "proportional_to_score":
        if score is None:
            missing_score_message = (
                "proportional_to_score needs a score: pass scores= to build_weights"
            )

            raise ValueError(missing_score_message)

        chosen = list(selected)
        raw = score.reindex(chosen).astype("float64")
        usable = raw[raw.notna() & (raw > 0.0)]

        if len(usable) == 0:

            return pandas.Series(dtype="float64")

        weights = usable / usable.sum()
    elif not LIBRARY_INSTALLED:
        missing_library_message = (
            f"{method!r} needs the Portfolio Construction library; only equal_weight runs alone"
        )

        raise ModuleNotFoundError(missing_library_message)
    else:
        import pyarrow

        import kaxanuk.portfolio_construction.entities
        import kaxanuk.portfolio_construction.sizing

        # The library reads a wide table -- a `date` column, then one column per security -- and
        # sizes the snapshot of tickers it is handed.  Every argument is keyword-only.
        dated_history = history.rename_axis("date")
        history_table = pyarrow.Table.from_pandas(
            dated_history.reset_index(),
            preserve_index=False,
        )
        allocator = kaxanuk.portfolio_construction.sizing.build_allocator(
            name=method,
            returns=history_table,
        )
        eligible_table = pyarrow.table(
            {
                "ticker": list(selected),
            }
        )
        snapshot = kaxanuk.portfolio_construction.entities.UniverseSnapshot(
            table=eligible_table,
        )
        allocated = allocator.allocate(
            snapshot=snapshot,
        )
        allocated_weights = kaxanuk.portfolio_construction.entities.Weights.from_allocated(
            allocated=allocated,
        )
        weights = pandas.Series(
            allocated_weights.as_mapping(),
        )

    if maximum_weight is None:

        return weights

    return weights.clip(upper=maximum_weight)


def _capped_proportional(
    values: "numpy.ndarray",
    maximum_weight: float,
) -> "numpy.ndarray":
    """
    Weights proportional to values sorted highest first, none above the cap, the excess spread.

    With the k largest capped, the rest share what is left in proportion; k is the smallest count
    for which the largest uncapped weight is within the cap.  When no count works -- too few names
    for the cap to place every dollar -- every name takes the cap.  An empty input is an empty book.
    """
    count = len(values)

    if count == 0:

        return numpy.zeros(0)

    tails = numpy.cumsum(values[::-1])[::-1]
    feasible = [
        capped
        for capped in range(count)
        if 1.0 - capped * maximum_weight > 0
        and values[capped] * (1.0 - capped * maximum_weight) / tails[capped]
        <= maximum_weight + 1e-12
    ]

    if len(feasible) == 0:

        return numpy.full(count, maximum_weight)

    capped_count = feasible[0]
    scale = (1.0 - capped_count * maximum_weight) / tails[capped_count]

    return numpy.concatenate([
        numpy.full(capped_count, maximum_weight),
        values[capped_count:] * scale,
    ])


def _drifted(
    weights: "pandas.Series",
    prices_then: "pandas.Series",
    prices_now: "pandas.Series",
) -> "pandas.Series":
    """
    Where last rebalance's weights stand now, after the prices moved and the cash stood still.

    A name with no price now drifts to nothing: it cannot be kept, only traded or sold by the
    engine at its last price.
    """
    held = weights[weights > 0]
    growth = prices_now.reindex(held.index) / prices_then.reindex(held.index)
    grown = held * growth
    cash = 1.0 - float(held.sum())
    total = float(grown.sum(skipna=True)) + cash
    shares = grown / total

    return shares.reindex(weights.index)

# --- example: end ---
