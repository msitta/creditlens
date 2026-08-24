# CreditLens

**Can you break down Brazilian corporate credit by company size? For part of the
market, no — and this is where that stops being true.**

SCR.data is the Central Bank of Brazil's public credit registry. It carries a
borrower-size field, which makes it tempting to slice lending by company size.
This project tests whether that field holds, and finds that it does not hold
evenly: it is reliable for banks and increasingly unreliable for fintechs.

The reason turns out to be more interesting than a data defect.

---

## The finding

In the most recent month of the series, the share of outstanding corporate credit
with **no borrower size on file** splits sharply by type of lender:

| Segment | Outstanding with no size on file |
|---|---|
| Bank | ~1% |
| Payment institution | ~11% |
| Fintech | ~31% |

Banks know the revenue of almost everything they lend to. Fintechs increasingly do
not — and the gap has widened steadily since 2022, from near zero.

**The empty field is not describing the borrower. It is describing the lender's
underwriting method.** A bank underwrites against declared revenue, which is why
that field is populated. A fintech underwriting against transaction flow — card
receivables, instant payments, invoice history — has no reason to capture revenue
at all. The missing value is a fingerprint of how the credit decision was made.

That reframing turns a data-quality nuisance into a readable signal: this series
measures how much corporate credit is being granted **without looking at revenue**,
and how fast that practice is spreading.

---

## Why this matters to anyone working with the data

Two practical consequences.

**If you consume SCR.data**, any analysis that filters or groups by borrower size
silently drops a growing share of fintech lending. The bias is not random: it is
concentrated in the fastest-growing segment. This repository documents where the
field can be trusted and where it cannot.

**If you hold a credit portfolio of your own**, the method transfers. The question
"which fields in my registry degrade, for which counterparties, and from when" is
answerable with the same approach: a control group that should not move, a
stability criterion that survives its own parameters, and an explicit statement of
what the data cannot answer.

---

## Method

The analysis is deliberately conservative, and the conservatism is declared rather
than assumed.

**Measured in outstanding value, not contract counts.** Counting rows treats a
ten-thousand and a ten-million contract as equal. The contract count is also
withheld for confidentiality in about 29% of rows, and what is missing is not
random — it concentrates in small cells.

**Suppressed cells are bounded, not dropped.** Where the contract count is withheld,
the cell is counted as holding at least one contract. Dropping those rows would
understate totals *more* in small segments — precisely the ones under study — which
would have biased the filter against fintechs for the wrong reason.

**A built-in control group.** Banks hold the overwhelming majority of the state's
corporate credit and sit flat at ~2% unavailable size across seven years, crossing
a pandemic and a full interest-rate cycle without moving. Whatever moves the fintech
line is not moving the bank line.

**A stability criterion that applies to everyone.** Months are excluded where a
single average-sized contract could shift the proportion by more than 0.1 percentage
points — roughly, where the segment has fewer than a thousand contracts. The rule is
applied identically to every segment; it removes fintech months from 2019 to early
2022, and no bank months at all. **The trend survives the filter**: the rise from
near zero to ~31% is still there using only months that pass.

---

## What this project does not claim

**The nationwide series has not been run yet.** The current extract is one state
(Paraná). Whether it is representative is untested and is declared as a limitation,
not assumed away.

**Payment institutions are not analysable here.** The stability criterion is
denominated in contract counts while the series is denominated in value. With value
concentrated in a few large contracts, that segment's proportion stays fragile even
in months the criterion approves. Rather than hide it behind a filter that does not
reach it, the segment is excluded and the reason stated. A value-denominated
criterion is the planned fix.

**The V1→V2 source migration has not been ruled out.** SCR.data changed collection
methodology mid-series. If the fintech rise aligns with that migration, the finding
could be a collection artefact rather than market behaviour. This is treated as a
veto condition, not a footnote: the diagnostic is designed and pending.

**A June 2024 discontinuity is unexplained.** The stability diagnosis independently
located a drop in fintech contract counts that month. The spike in the filtered
series at that same point is therefore suspect until the break is explained.

---

## What is in this repository

```
notebooks/01_unavailable_size.ipynb   analysis, end to end
estilo.py                             chart styling (Synthwave Horizon palette)
ingest.py                             month-by-month ingestion from SCR.data
DECISOES.md                           decision log — including rejected hypotheses
requirements.txt                      pinned dependencies
```

**`DECISOES.md` is worth reading alongside the analysis.** Every methodological
decision is recorded with its reasoning and — the part that matters — the condition
that would reverse it. It includes three hypotheses that were tested and did not
survive, and two cut-off criteria, one of which was discarded before it reached
production. The log is in Portuguese; an English version is planned.

---

## Reproducing

```bash
uv venv --python 3.12
.venv/Scripts/activate        # Windows;  source .venv/bin/activate on Unix
uv pip install -r requirements.txt
```

Raw SCR.data files are not versioned. `ingest.py` downloads and aggregates them;
the ingestion log in `data/processed/` records exactly which monthly files were
consumed.

---

## Data

SCR.data, Central Bank of Brazil, released under ODbL. The registry aggregates
credit operations reported by supervised institutions, with cell-level suppression
where counts are small enough to risk identification.

---

*Built by Marco Sitta — twenty years in corporate credit, now working in data.
The domain knowledge is the reason the empty field looked like a signal rather than
a defect.*
