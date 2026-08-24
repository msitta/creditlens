# Credit Granted Without Checking Revenue

**How much business credit in Paraná is granted without the borrower's revenue on file — and which kind of lender is driving the increase.**

Brazilian Central Bank credit registry (SCR.data) · corporate borrowers · state of Paraná · January 2019 – May 2026.

> **Status — work in progress.** The pipeline and the analysis run end to end, and the central finding is established. One methodological decision is still open (see *Open decision*), and two unexplained breaks in the series are still to be investigated.

## Context

For every credit operation it records, the SCR.data registry carries the borrower's size bracket — a field derived from declared revenue. In a meaningful share of records, that field is empty.

I started from a hypothesis drawn from twenty years inside Brazilian retail banking: that traditional banks cannot classify a relevant share of small businesses, pushing those companies toward more expensive credit elsewhere. It was a testable claim, so I tested it.

## What I found

**The original hypothesis does not hold.** Measured on active portfolio in the most recent month, the share of credit carrying no size bracket:

| Lender type | Credit with no revenue on file |
| --- | --- |
| Bank | 1% |
| Payment institution | 11% |
| Fintech | 31% |

Banks know the revenue of nearly everything they lend to. So the empty field does not describe the borrower — **it describes the lending method of whoever granted the credit.**

That turns the project into a different and better question: *how much credit is granted without looking at revenue at all, and how fast is that share growing?*

Across the seven-year series:

- **Banks** — flat at roughly 2%, through the pandemic and a complete interest-rate cycle. An almost perfect control line.
- **Fintechs** — from near zero, rising steadily. A trend, not noise.
- **Payment institutions** — 97%, then zero, then 37%. That is not economic behaviour. The segment barely existed in the state early in the series, and a proportion computed over a tiny portfolio moves entirely on a handful of contracts.

One caveat belongs next to every number above: banks dominate credit in this state. A high share inside fintechs and payment institutions is a large slice of a small whole. That does not invalidate the finding, but it has to be said alongside it.

## How I got there

Four decisions did most of the work. Each is recorded in [`DECISIONS.md`](DECISIONS.md) with its rationale and, deliberately, the condition that would reverse it.

- **`-1` is absence, not a value.** In `numero_de_operacoes`, `-1` marks statistical suppression for confidentiality. Averaging over it produces a wrong answer with no visible error. It is treated as missing — and a companion flag records where suppression occurred, because the suppression itself is information: it marks where operations are few.
- **Measured on `carteira_ativa`, not on row counts.** Counting rows treats a ten-thousand-real operation and a ten-million-real one as equal. `numero_de_operacoes` is incomplete in 28.9% of rows because of suppression, and what is missing is not random — it concentrates in the small cells. Balance in reais is the only one of the three available measures with no known bias here.
- **A market-share floor was rejected.** Fintechs are smaller than payment institutions, so any cut by relative size would drop both. The criterion has to target instability itself: how far a *single contract* moves the proportion in a given month.
- **Any threshold applies to every segment equally.** If it drops fintech months, those months go too.

## Open decision

The ceiling for `one_contract_impact_pp` — the point above which a month is considered unstable and leaves the chart — is not yet set. The diagnostic that informs it is built and plotted; the value and its rationale still have to be chosen and recorded in `DECISIONS.md`.

## Next steps

- Close the stability ceiling and record the decision.
- Investigate the breaks in row counts in June 2024 and July 2025. If they are methodology changes, the series has a seam and the trend needs a caveat.
- Break the analysis down to sub-regions of Paraná, which requires the Central Bank's separate dataset.
- Open it up by sector: where is revenue-blind lending growing fastest.

## Run it yourself

```bash
pip install -r requirements.txt
python src/ingest.py
```

`ingest.py` downloads SCR.data year by year from the Central Bank, filters to corporate borrowers in Paraná, coerces types, and writes a Parquet file to `data/processed/` along with an ingestion log. The raw archives and the processed dataset are not versioned — only the ingestion log is, so the pipeline can be audited without shipping hundreds of megabytes.

Then open `notebooks/01_missing_size_bracket.ipynb`.

## Data and licence

Source: [SCR.data](https://www.bcb.gov.br/estabilidadefinanceira/scrdata_serie), Banco Central do Brasil, published under the Open Database License (ODbL). Public data only — no customer-level or institution-level confidential information is used or reachable through this dataset.

## Author

**Marco Sitta** — Data & Business Analyst, after twenty years in Brazilian retail banking.
[LinkedIn](https://www.linkedin.com/in/marcositta) · msitta@gmail.com
