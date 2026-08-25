# Decision log

Each entry: what was decided, why, and what would make me change my mind.
A decision with no reversal condition is a well-written guess.

A revised entry is not deleted — it is amended, with a pointer to what replaced it. The trail is the asset.

---

## 2026-08-03 — Scope: corporate borrowers, Paraná, 2019 to 2026

**Why:** it fits a one-month deadline and it is the market I know at close range. Starting in 2019 gives a pre-pandemic baseline.

**What would change my mind:** if Paraná turns out to behave atypically against Brazil as a whole, the scope becomes a serious limitation and has to be declared as one.

> **Amended on 2026-08-20:** scope widened to nationwide. The Paraná denominator was too small for the fintech segment (0.07% of credit in the state), and a proportion over a small denominator is not stable — the same reasoning as the 1% floor.

---

## 2026-08-03 — Treat `-1` as absence, not as a value

**Why:** the `-1` in `numero_de_operacoes` is suppression for confidentiality, not a quantity. Summing or averaging over it produces a wrong result with no visible error. I also kept a column flagging where the suppression occurred, because that is itself information: it marks where operations are few.

**What would change my mind:** nothing. Keeping `-1` as a number is an error, not a choice.

---

## 2026-08-04 — Measure on `carteira_ativa`, not on counts

**Why:** counting rows treats a ten-thousand-real operation and a ten-million-real one as equal. `numero_de_operacoes` is incomplete in 28.9% of rows because of the suppression, and what is missing is not random — it concentrates in the small cells.
Balance in reais is the only one of the three measures with no known bias here.

**What would change my mind:** if the question became "how many companies", balance would not serve. But that question has no answer in this dataset.

---

## 2026-08-04 — Original hypothesis tested and rejected

**Hypothesis:** the traditional bank cannot classify a relevant share of small businesses, and they pay dearly for it.

**Test:** share of unavailable borrower size within each segment, in the most recent month.

**Result:** Bank 1%, Fintech 31%, Payment institution 11%. The bank knows the revenue of nearly every company it lends to. The hypothesis does not hold.

**What replaced it:** the empty field describes the method of whoever granted the credit, not the company. The series now measures how much credit is granted without looking at revenue, and how fast that phenomenon is growing.

---

## 2026-08-04 — A 1% floor for including a segment in the chart

**Why:** the payment-institution line swung between 97% and zero. On investigation, the cause is a small denominator: with a reduced portfolio, a handful of contracts shifts the whole proportion. A proportion without volume is not stable.

**How I applied it:** the floor applies to every segment, not only to the one I wanted to exclude. If it knocked out the fintech, I would have to accept that.

**What would change my mind:** if the segment grows past the floor, it comes back into the chart.

---

## 2026-08-24 — Nationwide scope carried into the code

**Why:** the amendment of 2026-08-20 widened the scope, but the code still carried `UF_KEEP = 'PR'` and the notebook still read the Paraná extract. The decision existed on paper only; the analysis was still one state.

**What changed:** `UF_KEEP = None` in `src/ingest.py`, and the notebook now reads `scrdata_pj_br.parquet`.

**What the change costs:** measured on one month, corporate rows go from 8,272 (Paraná) to 126,914 (nationwide) — a factor of 15.3. Over 89 months that is roughly 11.3 million rows. The ingestion accumulated every month as raw strings before coercing types, which does not fit in the memory available here; types are now coerced month by month, inside the loop. The notebook reads only the six columns the analysis uses.

**What is not yet true:** every figure in the notebook narrative — 1% / 11% / 31%, the bank flat at around 2% — was computed on Paraná. They stay labelled as Paraná until the nationwide series is actually run. Relabelling them without recomputing would be the exact error this log exists to prevent.

**What would change my mind:** if the nationwide run reproduces the same segment pattern, the Paraná cut was representative and the earlier limitation was conservative. If it does not, the earlier reading gets an amendment, not a quiet replacement.

---

## Open

**V1→V2 source version transition.** If the rise of `porte_indisponivel` in the fintech segment coincides with the methodological migration, the finding may reflect a change in collection rather than market behaviour. Test designed: mark the cut-off on the series and compare the two segments — if only the fintech moves, the version does not explain the phenomenon. Do not publish a conclusion before this.

**Unexplained movement in July 2025 on the bank line.** It weakens the argument for the bank as an immobile control in that specific month. Declared as an open caveat, not resolved.

---

## Template for the next ones

## YYYY-MM-DD — [decision]

**Why:**

**What would change my mind:**
