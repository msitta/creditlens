# Decision log

Each entry: what was decided, why, and what would make me change my mind.
A decision with no reversal condition is a well-written guess.

A revised entry is not deleted — it is amended, with a pointer to what replaced it. The trail is the asset.

---

## 2026-08-03 — Scope: business borrowers, Paraná, 2019 to 2026

**Why:** it fits a one-month deadline and it is the market I know at close range. Starting in 2019 gives a pre-pandemic baseline.

**What would change my mind:** if Paraná turns out to behave atypically against Brazil as a whole, the scope becomes a serious limitation and has to be declared as one.

> **Amended on 2026-08-20:** scope widened to nationwide. The Paraná denominator was too small for the fintech segment (0.07% of credit in the state), and a proportion over a small denominator is not stable — the same reasoning as the 1% floor.

---

## 2026-08-03 — Treat `-1` as absence, not as a value

**Why:** the `-1` in `numero_de_operacoes` is suppression for confidentiality, not a quantity. Summing or averaging over it produces a wrong result with no visible error. I also kept a column flagging where the suppression occurred, because that is itself information: it marks where operations are few.

**What would change my mind:** nothing. Keeping `-1` as a number is an error, not a choice.

> **Amended on 2026-09-11:** see "Suppressed cells count as at least one contract" below. Flagging the suppression was correct but incomplete — the flag also has to enter the denominator.

---

## 2026-08-04 — Measure on `carteira_ativa`, not on counts

**Why:** counting rows treats a ten-thousand-real operation and a ten-million-real one as equal. `numero_de_operacoes` is withheld in 37.2% of rows nationwide, and what is missing is not random — it concentrates in the small cells.
Balance in reais is the only one of the three measures with no known bias here.

**What would change my mind:** if the question became "how many companies", balance would not serve. But that question has no answer in this dataset.

---

## 2026-08-04 — Original hypothesis tested and rejected

**Hypothesis:** the traditional bank cannot classify a relevant share of small businesses, and they pay dearly for it.

**Test:** share of unavailable borrower size within each segment, in the most recent month.

**Result (Paraná, at the time):** Bank 1%, Fintech 31%, Payment institution 11%. The bank knows the revenue of nearly every company it lends to. The hypothesis does not hold.

**What replaced it:** the empty field describes the method of whoever granted the credit, not the company. The series now measures how much credit is granted without looking at revenue, and how fast that phenomenon is growing.

> **Confirmed nationwide on 2026-09-11:** `Banco` 3.1%, `Instituição de pagamento` 8.0%, `Fintech` 40.3%. The rejection holds and the gap is wider than the state-level cut showed.

---

## 2026-08-04 — A 1% floor for including a segment in the chart

**Why:** the payment-institution line swung between 97% and zero. On investigation, the cause is a small denominator: with a reduced portfolio, a handful of contracts shifts the whole proportion. A proportion without volume is not stable.

**How I applied it:** the floor applies to every segment, not only to the one I wanted to exclude. If it knocked out the fintech, I would have to accept that.

**What would change my mind:** if the segment grows past the floor, it comes back into the chart.

> **Superseded on 2026-09-11** by the stability threshold below. The floor was measuring the wrong thing.

---

## 2026-08-24 — Nationwide scope carried into the code

**Why:** the amendment of 2026-08-20 widened the scope, but the code still carried `UF_KEEP = 'PR'` and the notebook still read the Paraná extract. The decision existed on paper only; the analysis was still one state.

**What changed:** `UF_KEEP = None` in `src/ingest.py`, and the notebook now reads `scrdata_pj_br.parquet`.

**What the change costs:** the nationwide extract is 10,302,179 business-borrower rows over 90 months, drawn from 25,905,038 source rows. The ingestion accumulated every month as raw strings before coercing types, which does not fit in the memory available here; types are now coerced month by month, inside the loop. The notebook reads only the six columns the analysis uses.

**What is not yet true:** every figure in the notebook narrative — 1% / 11% / 31% — was computed on Paraná. They stay labelled as Paraná until the nationwide series is actually run. Relabelling them without recomputing would be the exact error this log exists to prevent.

**What would change my mind:** if the nationwide run reproduces the same segment pattern, the Paraná cut was representative and the earlier limitation was conservative. If it does not, the earlier reading gets an amendment, not a quiet replacement.

> **Closed on 2026-09-11:** the nationwide run reproduced the pattern, and the fintech figure came out higher than the state cut showed — 40.3% against 31%. The Paraná reading was representative and conservative. All figures in the notebook and README are now nationwide and labelled as such.

---

## 2026-09-11 — Stability threshold replaces the 1% market-share floor

*Decided during the nationwide run; logged today. Supersedes the entry of 2026-08-04.*

**Why the old rule was wrong:** the 1% floor excluded a segment for being **small**, not for being **unstable**. Those are different failures. `Fintech` holds 0.047% of business credit (median share) and is precisely the subject of the analysis — a rule that removes it for size removes the finding along with it. Market share is not a proxy for measurement reliability.

**The rule now:** a segment-month enters the chart when a single average-sized contract cannot move the proportion by more than a set number of percentage points.

```
max_shift_pp = 100 / min_contracts
```

Ceiling set at **0.1 pp**, roughly 1,000 contracts in the cell. Months kept: `Banco` 90 of 90, `Fintech` 71 of 90, `Instituição de pagamento` 64 of 90.

**Why 0.1 pp, and why the number matters less than it looks.** The series moves in tens of percentage points, so a ceiling two orders of magnitude below the smallest movement worth reading means no plotted month can have been produced by contract-level noise. But the choice is reported with its sensitivity rather than defended on its own:

| Ceiling | Months kept | Starts | First % | Last % | Slope, pp/year |
|---|---:|---|---:|---:|---:|
| 0.05 pp | 69 | 2020-10 | 0.0 | 40.3 | 8.90 |
| 0.10 pp *(used)* | 71 | 2020-08 | 5.0 | 40.3 | 8.52 |
| 0.25 pp | 79 | 2019-12 | 0.1 | 40.3 | 7.55 |
| 0.50 pp | 80 | 2019-11 | 0.0 | 40.3 | 7.45 |
| 1.00 pp | 84 | 2019-07 | 0.0 | 40.3 | 7.05 |
| no filter | 84 | 2019-07 | 0.0 | 40.3 | 7.05 |

Tightening the ceiling costs months and *steepens* the slope. There is no setting at which the rise disappears.

**How I applied it:** same ceiling for every segment, no exceptions.

**What would change my mind:** if the finding survived at only one ceiling. The table above is the test, and it is in the notebook so anyone can re-run it with different values.

---

## 2026-09-11 — Suppressed cells count as at least one contract

*Decided during the nationwide run; logged today.*

**Why:** a cell with `numero_de_operacoes = -1` is suppressed because it is small, not because it is empty. Treating it as zero contracts pushed the stability metric toward infinity for exactly those cells, which then failed the threshold and dropped out. Since suppression concentrates in small cells — 75.3% of fintech cells against 31.5% of bank cells — the rule was excluding the segment under study through a side door.

**The rule now:** a suppressed cell contributes at least one contract to the denominator.

**What this makes each number:** the contract total is a **floor** — the true count is at least that. The displacement metric is a **ceiling with respect to the arithmetic** and a **floor with respect to reality**: value is more concentrated than count, so one large contract shifts the proportion by more than 1/N. The metric bounds the average case, not the worst case, and that limit is stated in the notebook rather than left for a reader to find.

**What would change my mind:** if the Central Bank published the suppression threshold, the floor could be replaced by the actual minimum instead of 1.

---

## 2026-09-11 — Names that come from the source are never renamed

*Reverses an earlier working rule that translated column names to English on load.*

**The earlier rule:** segment values stayed in Portuguese, column names were aliased to English at load time. It held for a while and it was wrong.

**Why it was wrong:** it drew a line I could not defend under questioning. Asked "why is `segmento` sacred and `carteira_ativa` not?", the honest answer was that one felt more like data than the other. That is not a criterion.

**The rule now, and it is one rule:** anything published by the Central Bank keeps the name the Central Bank gives it — column names and values alike. Anything the analysis produces is named by the analyst, in English. So `df['carteira_ativa']` and `'Instituição de pagamento'` are untranslated; `unavailable_share_%`, `max_shift_pp` and `min_contracts` are mine and are in English.

**What it buys:** someone reading this repository and searching SCR.data for a name used here finds it. Under the previous rule they would have searched for `outstanding` and found nothing. In a project whose entire argument is that a relabelled field misleads its consumer, renaming the source fields was the argument working against itself.

**What it costs:** the notebook narrative reads in two languages. `COLUMNS` stops being a rename map and becomes a glossary — it still selects the six columns loaded, and now also documents what each one means.

**What would change my mind:** if the Central Bank published an official English vocabulary for SCR.data, that becomes the name to use — because it would then be the source's own name, not my translation of it.

---

## 2026-09-11 — Charts do not rely on colour alone

**Why:** the palette assigns cyan to `Banco`, pink to `Fintech` and orange to `Instituição de pagamento`. Measured as relative luminance, cyan and orange sit **1.13:1** apart — effectively the same shade once colour is removed. Pink and orange are 1.61:1, cyan and pink 1.81:1. The worst pair is the reference series and the unstable one, which is exactly the comparison every chart in this repository asks the reader to make.

That breaks the chart for anyone reading it printed in greyscale, on a monochrome e-reader, or with red-green colour blindness — around 8% of men.

**What changed:** `style.dash()` gives the orange series a dashed line, applied after plotting. Line style is a redundant channel: the distinction survives when colour does not. The palette itself is unchanged — it is the project's visual identity and the problem was never the colours, it was relying on them as the only carrier.

**A detail worth recording:** `dash()` matches on colour, not on column order. The filtered chart draws six lines for three columns, because the raw series is ghosted underneath it. Matching by position would have dashed the ghost and left the real line solid — correct-looking code producing a wrong chart.

**What would change my mind:** nothing about the principle. If the palette changes, the luminance figures have to be recomputed and the redundant channel reassigned to whichever pair collapses.

---

## 2026-09-11 — The December 2023 peak in the bank line is seasonal

*Investigated during the nationwide run; logged today.*

**Why it mattered:** the bank line is the reference in this analysis. A spike in the reference weakens every comparison around it.

**Three checks:**

1. **Numerator or denominator?** In December 2023 the bank's total book grew 3.4% while credit with no size on file grew 30.1%. The share rose because unclassified credit came in, not because the book shrank.
2. **Systematic or one-off?** December exceeds November in six of the seven years in the series. The exception is 2020, by 0.07 pp — inside noise.
3. **One product or the whole book?** Spread across the book. The largest single move is `Outros créditos` at +1.97 pp, but it carries 11.7% of the December book; `Empréstimos`, at 40.2% of the book, moves +0.80 pp. No product accounts for the peak.

**Conclusion:** year-end reporting behaviour, not a break in the series and not specific to any lending product.

**What would change my mind:** a December without the peak, or a year where one product explains the whole move.

---

## 2026-09-11 — The V1→V2 methodology transition does not affect this series

*Closes the open item declared on 2026-08-24.*

**The worry:** the Central Bank publishes two methodology documents for SCR.data. If the rise in `porte_indisponivel` coincided with the migration, the finding would describe a change in how the data is collected rather than a change in how credit is granted. That would invalidate the project.

**What I checked, and what I did not find.** The V2 methodology document contains **no** version history, **no** changelog, and **no** statement that the V1-era series was reprocessed. I am recording that explicitly, because the tempting shortcut was to assume the document said something reassuring that it does not say. The absence is the finding.

**What actually closes it — three independent lines, all reproducible from this repository:**

1. **No V1-era file is in the dataset.** `src/ingest.py` fetches `scrdata_{year}.zip` from the current Central Bank endpoint for every year 2019–2026, in a single run. All 90 months were served by the publication pipeline as it stands today. There is no seam between two vintages of file, because only one vintage was ever downloaded.
2. **No structural break in the volumes.** The ingestion log records rows read and rows retained per monthly file. The two largest movements in the whole series are March 2019 (+5.1% read, +1.1% retained) and July 2025 (−4.6% read, −1.0% retained). Both are inside ordinary month-to-month variation, and in both the retained share moves by less than the read volume — the opposite of what a scope change would produce.
3. **The only dated rule in V2 does not touch the measured fields.** V2 declares that from January 2025 onward, only operations flagged by the institution as problem assets are counted (special characteristic 19). That rule governs `ativo_problematico`. This analysis measures `porte` and `carteira_ativa`. The discontinuity is real and documented — it is simply in a different column.

**What this does not claim.** It does not claim the underlying reporting by institutions was homogeneous over seven years. It claims that no discontinuity attributable to the SCR.data publication itself sits inside the window this series measures.

**What would change my mind:** the Central Bank publishing a changelog that contradicts point 3, or a republication of the annual archives that changes the volumes in point 2. Both are checkable by re-running the ingestion and diffing the log.

---

## Open

**Unexplained movement in July 2025 on the bank line.** Downgraded from a veto condition to an observation. The entry above establishes that the file composition did not change materially that month, so whatever moved is in the data rather than in the collection. Across the cut, `Banco` moves 0.32 pp while `Fintech` moves 8.52 pp and `Instituição de pagamento` moves 3.83 pp — an order of magnitude apart, which is why the bank remains usable as a reference. It is still movement in what should be inert, and it is still unexplained. Declared as a caveat in the README; not a reason to withhold the finding.

**A June 2024 discontinuity in fintech contract counts.** Located by the stability diagnosis. The volume checks in the entry above were run on whole monthly files, not on fintech cells, so they do not speak to this. Open.

**Stability criterion denominated in contracts, series denominated in value.** The threshold is expressed in contract counts while the line it filters is expressed in outstanding balance. The mismatch is deliberate — contracts are the right unit for asking whether a proportion is stable — but it bites hardest where value concentrates in few large contracts, which is the payment-institution case: that segment's mean `max_shift_pp` is 2.99 against the fintech's 0.055. A value-denominated criterion is the planned fix.

**Excluded months mix two different things.** Of the 19 fintech months not plotted, some are months the segment has no data for at all (84 segment-months exist out of 90) and the rest are months the criterion rejects. The chart draws the raw series faintly underneath the filtered one so the difference is visible, but the counts in the README do not separate the two causes.

**Delinquency spread hypothesis.** Comparing delinquency rates between the `porte` informed and `porte indisponível` groups, within each segment and month. Deprioritised, not rejected. A naive time-series correlation here would be spurious — common trend, shared denominator, compositional confounding by segment — so the correct form is a segment-controlled spread on first differences. Out of scope until the core deliverable ships.

**State-level breakdown; the 2019–2020 collapse in the bank line.** Queued for a later section.

---

## Template for the next ones

## YYYY-MM-DD — [decision]

**Why:**

**What would change my mind:**
