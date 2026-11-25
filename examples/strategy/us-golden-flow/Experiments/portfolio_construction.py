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

import collections.abc
import functools
import importlib.util
import pathlib

import numpy
import pandas
import pyarrow

__all__ = [
    "LIBRARY_INSTALLED",
    "banded_book",
    "bounded_book",
    "bounded_by_score",
    "bounded_by_score_and_sector",
    "bounded_by_score_and_sector_with_library",
    "bounded_by_score_with_library",
    "build_weights",
    "delisting_top_up_dates",
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
# The repository's keys, read into the environment by name before the library's first call.
ENVIRONMENT_PATH = pathlib.Path(__file__).parent.parent / "Config" / ".env"
# How many times the library's name cap and group cap are applied in turn before the book is read;
# each pass moves what the other freed, and a few settle any book this rule holds.
LIBRARY_CAP_PASSES = 50
# The dimension the library's classification names the sector under.
SECTOR_DIMENSION = "sector"
# The sector of a name the sector map does not carry: a group of its own, capped like the rest.
UNCLASSIFIED_SECTOR = "unclassified"


def banded_book(
    targets: "pandas.DataFrame",
    decision_prices: "pandas.DataFrame",
    fill_prices: "pandas.DataFrame",
    band: float,
    *,
    maximum_weight: float = 1.0,
    sectors: "collections.abc.Mapping[str, str] | None" = None,
    sector_maximum: float = 1.0,
    invested: float = 1.0,
    top_up_dates: "pandas.DatetimeIndex | None" = None,
    top_up_scores: "pandas.DataFrame | None" = None,
) -> "pandas.DataFrame":
    """
    The book actually struck on each rebalance date: the target, except where a trade is too small.

    On each of `top_up_dates` between the targets' dates, a fund's housekeeping instead of a
    rebalance: what the names whose prices stopped were worth goes back into the names still held,
    in proportion to `top_up_scores` at that date (equally when none are given), into what each has
    left under `maximum_weight` and each sector under `sector_maximum`.  Every other held name is
    written as it drifted to the fill, so nothing is sold and nothing new is bought.  A name with no
    price that day is valued at its last fill price, the cash the engine sold it for.

    A name held since the last rebalance and still in the target keeps the weight it drifted to
    when its target differs from that weight by no more than `band`; every other name -- an entry,
    an exit, a held name whose target moved further -- is traded.  The decision is made on
    `decision_prices`, the close before the fill, so it uses nothing the person placing the orders
    could not see; the kept weight is then written as it stands at `fill_prices`, the fill, which is
    how "leave this name alone" is said in a weight file.

    The traded names share what the kept names leave of a book invested to `invested`, in
    proportion to their targets: what the kept names hold over their targets comes out of the
    traded names, and what they hold under it goes into them, by the owner's decision of
    2026-11-17, so the band leaves no cash of its own.  The first date is the target scaled to
    `invested`; the rest of each book is the cash the owner chose to hold.  The traded names stay
    inside the target's bounds -- none above `maximum_weight`, no sector of `sectors` above
    `sector_maximum` with its kept names counted -- and what no traded name can take is cash.
    Cash is carried flat between rebalances: its interest is the engine's, and a few basis points
    of it moves no decision.
    """
    extra_dates = pandas.DatetimeIndex([]) if top_up_dates is None else top_up_dates
    housekeeping = set(extra_dates.difference(targets.index))
    all_dates = targets.index.union(extra_dates)
    dates = list(all_dates.sort_values())
    carried_prices = fill_prices.ffill()
    sector_of = _sector_labels(
        targets.columns,
        sectors or {},
    )
    struck_rows = {
        dates[0]: targets.loc[dates[0]] * invested,
    }

    for previous_date, date in zip(
        dates[:-1],
        dates[1:],
        strict=True,
    ):
        previous_weights = struck_rows[previous_date]

        if date in housekeeping:
            struck_rows[date] = _topped_up(
                previous_weights,
                carried_prices.loc[previous_date],
                carried_prices.loc[date],
                fill_prices.loc[date].notna(),
                None if top_up_scores is None else top_up_scores.loc[date],
                maximum_weight,
                sector_of,
                sector_maximum,
            )
            continue

        target = targets.loc[date]
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
        traded = _traded_into_room(
            target.where(~kept, 0.0),
            at_fill.where(kept, 0.0).fillna(0.0),
            maximum_weight,
            sector_of,
            sector_maximum,
            invested,
        )
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
    weigher: "collections.abc.Callable[..., pandas.Series] | None" = None,
) -> "pandas.DataFrame":
    """
    The target book on every date: the eligible names by score, the bounds setting how many.

    The score is cut here, once, to the value it had at the close before each date -- the matrix
    is moved one row down its own calendar, which is the panel's trading calendar -- so no notebook
    writes a `.shift(1)` of its own.  Each date is then sized by `bounded_by_score`.  The book on
    every date, not only on rebalance dates, is what lets a rule re-strike exactly when the held set
    changes.  `weigher` sizes each date, `bounded_by_score` when none is named;
    `bounded_by_score_with_library` builds the same book with the Portfolio Construction library.
    """
    sizing = bounded_by_score if weigher is None else weigher
    scores_before = scores.shift(1)
    rows = {}

    for date in eligibility.index:
        eligible = eligibility.loc[date]
        names = eligible.index[eligible.to_numpy(dtype=bool)]
        score = scores_before.loc[date, names]
        rows[date] = sizing(
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


def bounded_by_score_and_sector(
    score: "pandas.Series",
    maximum_weight: float,
    minimum_weight: float,
    sectors: "collections.abc.Mapping[str, str]",
    sector_maximum: float,
) -> "pandas.Series":
    """
    `bounded_by_score`, with no sector above `sector_maximum` either.

    Names are taken in order of score, ties by name.  Each is added to the book if, sized with the
    names already in it, no weight falls below `minimum_weight`; otherwise it is skipped and the
    next is tried.  With the name cap alone, a name that fails makes every later one fail too, so
    skipping gives `bounded_by_score`'s book; with the sector cap, a name in a full sector can fail
    while one in another sector still fits, and stopping would leave in cash what that one could
    hold.  A book is sized by filling -- every name proportional to its score, a name above the cap
    held at it, a sector above its cap scaled down to it, what either frees spread over the names
    still free -- and what no free name can take is left uninvested.  A name with no sector in
    `sectors` is a sector of its own, `unclassified`, capped like any other.  Pass it to
    `bounded_book` with `functools.partial`, naming `sectors` and `sector_maximum`.
    """
    ordered = _ordered_by_score(score)
    labels = _sector_labels(
        ordered.index,
        sectors,
    )
    codes = pandas.factorize(labels)[0]
    values = ordered.to_numpy(dtype=float)
    held = []

    for position in range(len(values)):
        trial = [*held, position]
        trial_weights = _capped_by_name_and_sector(
            values[trial],
            codes[trial],
            maximum_weight,
            sector_maximum,
        )

        if trial_weights.min() >= minimum_weight:
            held.append(position)

    weights = _capped_by_name_and_sector(
        values[held],
        codes[held],
        maximum_weight,
        sector_maximum,
    )

    return pandas.Series(
        weights,
        index=ordered.index[held],
        dtype=float,
    )


def bounded_by_score_and_sector_with_library(
    score: "pandas.Series",
    maximum_weight: float,
    minimum_weight: float,
    sectors: "collections.abc.Mapping[str, str]",
    sector_maximum: float,
) -> "pandas.Series":
    """
    The names `bounded_by_score_and_sector` holds, sized by the Portfolio Construction library.

    The library's `feature_weighting`, proportional to the score, then `Weights.cap` and
    `Weights.cap_groups` in turn until neither moves a weight.  The library has no floor that picks
    names, so the names are the notebook's; what is checked is the sizing.  The library places
    every dollar or refuses, so a book whose caps cannot hold it all -- too few names outside a
    capped sector -- keeps the notebook's own weights, which leave the rest in cash.  A date on
    which the two disagree is a finding.
    """
    notebook_book = bounded_by_score_and_sector(
        score,
        maximum_weight,
        minimum_weight,
        sectors,
        sector_maximum,
    )
    labels = _sector_labels(
        notebook_book.index,
        sectors,
    )

    return _library_capped_by_name_and_sector(
        score.reindex(notebook_book.index),
        labels,
        maximum_weight,
        sector_maximum,
    )


def bounded_by_score_with_library(
    score: "pandas.Series",
    maximum_weight: float,
    minimum_weight: float,
) -> "pandas.Series":
    """
    `bounded_by_score`, with each count sized by the KaxaNuk Portfolio Construction library.

    The walk is the same -- names in order of score, ties by name, the count growing while the
    smallest weight stays at or above `minimum_weight` -- because the library has no floor that sets
    a count.  What the library does is the sizing: its `feature_weighting` method, proportional to
    the score, then `Weights.cap`, which spreads what the cap frees over the other names until none
    is above it.  With too few names for the cap to place every dollar, the cap cannot hold and the
    library refuses it, so each name takes the cap and the rest is left uninvested, as the
    blueprint says.  It exists to check that the library builds this book: a date on which the two
    weighers disagree is a finding.
    """
    usable = score[score > 0].dropna()
    by_name = usable.sort_index()
    ordered = by_name.sort_values(
        ascending=False,
        kind="mergesort",
    )
    counts = range(1, len(ordered) + 1)
    first_failing = next(
        (
            count
            for count in counts
            if _library_capped_proportional(ordered.iloc[:count], maximum_weight).min()
            < minimum_weight
        ),
        None,
    )
    held_count = len(ordered) if first_failing is None else first_failing - 1
    weights = _library_capped_proportional(
        ordered.iloc[:held_count],
        maximum_weight,
    )

    return weights


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


def delisting_top_up_dates(
    targets: "pandas.DataFrame",
    fill_prices: "pandas.DataFrame",
) -> "pandas.DatetimeIndex":
    """
    The days a book puts a delisted name's cash back to work: two trading days after its last price.

    A name held on a target date whose prices stop before the next one is sold by the engine at its
    last price, on day L.  That the price stopped is known only at the close of L+1, when none came,
    so the top-up's orders go in at the open of L+2.  A top-up that would fall on or after the next
    target date is that date's rebalance, and a name still priced on the last day of the prices is
    not delisted.  The held names are the target's: the band only ever holds a name in the target.
    """
    calendar = fill_prices.index
    last_priced = fill_prices.apply(pandas.Series.last_valid_index)
    starts = list(targets.index)
    ends = [*starts[1:], pandas.Timestamp.max]
    found = set()

    for start, end in zip(
        starts,
        ends,
        strict=True,
    ):
        held = targets.columns[targets.loc[start].to_numpy() > 0]

        for name in held:
            last = last_priced.get(name)

            if last is None or pandas.isna(last) or last >= calendar[-1] or last < start:
                continue

            position = calendar.get_loc(last) + 2

            if position < len(calendar) and calendar[position] < end:
                found.add(calendar[position])

    return pandas.DatetimeIndex(sorted(found))


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


def _capped_by_name_and_sector(
    values: "numpy.ndarray",
    groups: "numpy.ndarray",
    maximum_weight: float,
    sector_maximum: float,
    budget: float = 1.0,
    group_rooms: "numpy.ndarray | None" = None,
) -> "numpy.ndarray":
    """
    Weights proportional to values, no name above `maximum_weight`, no group above `sector_maximum`.

    Filling: the free names share what is left of `budget` in proportion to their values; a name
    above the cap is fixed at it; a group above its room has every name in it scaled down to the
    room and fixed.  A group's room is `sector_maximum` unless `group_rooms` gives one per group,
    in the order of the sorted group labels, which is how the band counts what its kept names
    already hold.  Each pass fixes at least one name, so the loop ends; what no free name is left
    to take stays uninvested.  An empty input is an empty book.
    """
    count = len(values)
    weights = numpy.zeros(count)
    free = numpy.ones(
        count,
        dtype=bool,
    )
    labels, codes = numpy.unique(
        groups,
        return_inverse=True,
    )
    full_rooms = numpy.full(
        len(labels),
        sector_maximum,
    )
    rooms = full_rooms if group_rooms is None else group_rooms
    tolerance = 1e-12

    for _ in range(2 * count + 1):
        if not free.any():
            break

        left = budget - float(weights[~free].sum())
        shares = left * values[free] / float(values[free].sum())
        weights[free] = shares
        over_name = free & (weights > maximum_weight + tolerance)

        if over_name.any():
            weights[over_name] = maximum_weight
            free[over_name] = False
            continue

        totals = numpy.bincount(
            codes,
            weights=weights,
            minlength=len(labels),
        )
        over_sector = numpy.flatnonzero(totals > rooms + tolerance)

        if len(over_sector) == 0:
            break

        for code in over_sector:
            in_group = codes == code
            weights[in_group] = weights[in_group] * rooms[code] / float(totals[code])
            free[in_group] = False

    return weights


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


def _library_capped_by_name_and_sector(
    score: "pandas.Series",
    groups: "numpy.ndarray",
    maximum_weight: float,
    sector_maximum: float,
) -> "pandas.Series":
    """
    The library's book for one count: proportional, then the name cap and the group cap in turn.

    Where the caps cannot hold the whole book, the library refuses, and the count is sized by
    `_capped_by_name_and_sector` instead, which leaves the rest in cash.
    """
    if len(score) == 0:

        return pandas.Series(dtype=float)

    names_per_group = pandas.Series(groups).value_counts()
    group_room = names_per_group.clip(upper=sector_maximum / maximum_weight)
    capacity = float(group_room.sum()) * maximum_weight

    if capacity < 1.0 or len(score) * maximum_weight < 1.0:
        own = _capped_by_name_and_sector(
            score.to_numpy(dtype=float),
            groups,
            maximum_weight,
            sector_maximum,
        )

        return pandas.Series(
            own,
            index=score.index,
            dtype=float,
        )

    import kaxanuk.portfolio_construction.entities

    proportional = _library_capped_proportional(
        score,
        maximum_weight,
    )
    classification = kaxanuk.portfolio_construction.entities.Classification(
        assignments={
            SECTOR_DIMENSION: {
                str(identifier): str(group)
                for identifier, group in zip(
                    score.index,
                    groups,
                    strict=True,
                )
            },
        },
    )
    limits = {
        str(group): sector_maximum
        for group in sorted(set(groups))
    }
    passes = [
        kaxanuk.portfolio_construction.entities.Weights.from_table(
            table=_weight_table(proportional),
            weight_column="weight",
        ),
    ]

    for _ in range(LIBRARY_CAP_PASSES):
        grouped = passes[-1].cap_groups(
            classification=classification,
            dimension=SECTOR_DIMENSION,
            limits=limits,
        )
        passes.append(grouped.cap(maximum=maximum_weight))
        before = pandas.Series(passes[-2].as_mapping())
        after = pandas.Series(passes[-1].as_mapping())
        difference = (after - before).abs()

        if float(difference.max()) < 1e-12:
            break

    weights = pandas.Series(
        passes[-1].as_mapping(),
        dtype=float,
    )

    return weights.reindex(score.index)


def _library_capped_proportional(
    score: "pandas.Series",
    maximum_weight: float,
) -> "pandas.Series":
    """
    Weights proportional to the score, none above the cap, sized by the Portfolio Construction
    library: `feature_weighting`, proportional, then `Weights.cap`.  Too few names for the cap to
    place every dollar take the cap each; an empty score is an empty book.
    """
    if len(score) == 0:

        return pandas.Series(dtype=float)

    if len(score) * maximum_weight < 1.0:

        return pandas.Series(
            maximum_weight,
            index=score.index,
            dtype=float,
        )


    import kaxanuk.portfolio_construction.entities
    import kaxanuk.portfolio_construction.enums.weighting_method
    import kaxanuk.portfolio_construction.sizing

    _load_licence()
    snapshot_table = pyarrow.table({
        "ticker": [
            str(identifier)
            for identifier in score.index
        ],
        "score": score.to_numpy(dtype=float),
    })
    snapshot = kaxanuk.portfolio_construction.entities.UniverseSnapshot(table=snapshot_table)
    configuration = kaxanuk.portfolio_construction.sizing.FeatureWeightingAllocatorConfig(
        feature_column="score",
        method=kaxanuk.portfolio_construction.enums.weighting_method.WeightingMethod.PROPORTIONAL,
    )
    allocator = kaxanuk.portfolio_construction.sizing.build_allocator(
        name="feature_weighting",
        config=configuration,
    )
    allocated = allocator.allocate(snapshot=snapshot)
    proportional = kaxanuk.portfolio_construction.entities.Weights.from_allocated(
        allocated=allocated,
    )
    capped = proportional.cap(maximum=maximum_weight)
    weights = pandas.Series(
        capped.as_mapping(),
        dtype=float,
    )

    return weights.reindex(score.index)


@functools.cache
def _load_licence() -> bool:
    """
    Put the repository's `Config/.env` in the environment once, where the library reads its key.

    The library looks for `KNPC_API_KEY_KAXANUK` in the environment or a `.kaxanuk_license` file,
    never in `Config/.env`; a variable already set wins.  Nothing is printed.
    """
    import dotenv

    loaded = dotenv.load_dotenv(
        ENVIRONMENT_PATH,
        override=False,
    )

    return loaded


def _ordered_by_score(
    score: "pandas.Series",
) -> "pandas.Series":
    """
    The names with a positive score, highest first, ties broken by name.
    """
    usable = score[score > 0].dropna()
    by_name = usable.sort_index()

    return by_name.sort_values(
        ascending=False,
        kind="mergesort",
    )


def _poured_into_room(
    held: "pandas.Series",
    scores: "pandas.Series",
    amount: float,
    maximum_weight: float,
    sector_of: "pandas.Series",
    sector_maximum: float,
) -> "pandas.Series":
    """
    What each held name receives of `amount`: in proportion to its score, inside both caps' room.

    A name's room is what it has left under `maximum_weight`, a sector's what it has left under
    `sector_maximum`, both counted on the weights the names already hold.  A pass hands what is left
    to the names with room, cuts each to its own room and each sector to its room, and goes again on
    what that left over; a name or a sector that fills drops out, so the passes end.  What no name
    has room for stays uninvested.
    """
    added = pandas.Series(
        0.0,
        index=held.index,
    )
    tolerance = 1e-12

    for _ in range(2 * len(held) + 1):
        left = amount - float(added.sum())
        name_room = (maximum_weight - held - added).clip(lower=0.0)
        sector_totals = (held + added).groupby(sector_of).sum()
        sector_room = (sector_maximum - sector_totals).clip(lower=0.0)
        has_room = (
            (name_room > tolerance)
            & (sector_of.map(sector_room) > tolerance)
            & (scores > 0)
        )

        if left <= tolerance or not has_room.any():
            break

        room_total = float(scores[has_room].sum())
        shares = scores.where(has_room, 0.0) / room_total
        offered = (shares * left).clip(upper=name_room)
        offered_by_sector = offered.groupby(sector_of).sum()
        offered_sectors = offered_by_sector.where(offered_by_sector > 0)
        sector_scale = (sector_room / offered_sectors).clip(upper=1.0)
        given = offered * sector_of.map(sector_scale.fillna(1.0))
        added.loc[:] = added + given

    return added


def _sector_labels(
    identifiers: "pandas.Index",
    sectors: "collections.abc.Mapping[str, str]",
) -> "numpy.ndarray":
    """
    Each identifier's sector, `unclassified` where the map has none.
    """
    labels = [
        sectors.get(str(identifier), UNCLASSIFIED_SECTOR)
        for identifier in identifiers
    ]

    return numpy.array(
        labels,
        dtype=object,
    )


def _topped_up(
    previous_weights: "pandas.Series",
    prices_then: "pandas.Series",
    prices_now: "pandas.Series",
    priced_now: "pandas.Series",
    scores: "pandas.Series | None",
    maximum_weight: float,
    sector_of: "numpy.ndarray",
    sector_maximum: float,
) -> "pandas.Series":
    """
    The book on a top-up date: as it drifted, with the delisted names' cash poured into the rest.

    The prices carry each name's last price forward, so a name sold at its last price still counts
    in the book's value, as the cash it became; that value is what `_poured_into_room` hands out.
    """
    drifted = _drifted(
        previous_weights,
        prices_then,
        prices_now,
    ).fillna(0.0)
    stopped = (drifted > 0) & ~priced_now.reindex(drifted.index, fill_value=False)
    freed = float(drifted[stopped].sum())
    kept = drifted.where(~stopped, 0.0)
    held_names = kept.index[kept.to_numpy() > 0]
    held_scores = (
        pandas.Series(1.0, index=held_names)
        if scores is None
        else scores.reindex(held_names).fillna(0.0)
    )
    sector_labels = pandas.Series(
        sector_of,
        index=drifted.index,
    )
    added = _poured_into_room(
        kept[held_names],
        held_scores,
        freed,
        maximum_weight,
        sector_labels[held_names],
        sector_maximum,
    )

    return kept.add(
        added,
        fill_value=0.0,
    )


def _traded_into_room(
    traded_targets: "pandas.Series",
    kept_weights: "pandas.Series",
    maximum_weight: float,
    sector_of: "numpy.ndarray",
    sector_maximum: float,
    invested: float,
) -> "pandas.Series":
    """
    The traded names' weights: what the kept names leave of a book invested to `invested`.

    The kept names' weight comes off the top, and off each sector's room; the traded names then
    fill the rest in proportion to their targets, inside the name and sector caps.  A sector its
    kept names already fill to the cap leaves its traded names nothing, which only kept names that
    drifted up can cause.
    """
    trading = (traded_targets > 0).to_numpy()
    weights = pandas.Series(
        0.0,
        index=traded_targets.index,
    )

    if not trading.any():
        return weights

    labels, codes = numpy.unique(
        sector_of,
        return_inverse=True,
    )
    kept_by_sector = numpy.bincount(
        codes,
        weights=kept_weights.to_numpy(),
        minlength=len(labels),
    )
    rooms = numpy.clip(
        sector_maximum - kept_by_sector,
        0.0,
        None,
    )
    trading_labels = numpy.unique(sector_of[trading])
    trading_rooms = rooms[numpy.searchsorted(labels, trading_labels)]
    kept_total = float(kept_weights.sum())
    filled = _capped_by_name_and_sector(
        traded_targets.to_numpy()[trading],
        sector_of[trading],
        maximum_weight,
        sector_maximum,
        budget=max(0.0, invested - kept_total),
        group_rooms=trading_rooms,
    )
    weights[trading] = filled

    return weights


def _weight_table(
    weights: "pandas.Series",
) -> "pyarrow.Table":
    """
    A book as the table `Weights.from_table` reads: a ticker and a weight column.
    """

    return pyarrow.table({
        "ticker": [
            str(identifier)
            for identifier in weights.index
        ],
        "weight": weights.to_numpy(dtype=float),
    })

# --- example: end ---
