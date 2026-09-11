# CreditLens

**Can you break down Brazilian business credit by company size? For part of the
market, no — and this is where that stops being true.**

SCR.data is the Central Bank of Brazil's public credit registry. It carries a
borrower-size field, which makes it tempting to slice lending by company size.
This project tests whether that field holds, and finds that it does not hold
evenly: it degrades sharply and predictably by type of lender.

The reason turns out to be more interesting than a data defect.

> **A note on terms.** SCR.data splits borrowers into individuals and legal
> entities. This project covers the legal-entity side, called **business
> borrowers** throughout — no size implied, which is the whole point. Writing
> *corporate* would smuggle in the size the data is being asked to prove. It is
> also why *non-financial corporations* is not used: the ECB term excludes
> financial institutions and the SCR.data axis does not.
>
> Segment names stay in Portuguese, exactly as the Central Bank publishes them.
> Translating `Banco` to `Bank` would mean this repository no longer matches its
> source, and anyone searching SCR.data for a label used here would find nothing.
> A glossary is at the end.

**Scope:** 90 months, January 2019 to June 2026, nationwide. 25.9 million source
rows, 10.3 million business-borrower rows retained.

---

## The finding

In June 2026, the share of outstanding business credit with **no borrower size on
file** splits sharply by type of lender:

| Segmento | Outstanding, BRL bn | No size on file, BRL bn | Share with no size | Months passing the filter |
|---|---:|---:|---:|---:|
| Fintech | 2.1 | 1.4 | **40.3%** | 71 of 90 |
| Instituição de pagamento | 5.7 | 0.5 | 8.0% | 64 of 90 |
| Financeira | 59.0 | 4.7 | 7.4% | — |
| Desenvolvimento/Fomento | 379.0 | 26.1 | 6.4% | — |
| Cooperativa | 233.2 | 7.9 | 3.3% | — |
| Banco | 2,140.0 | 67.8 | 3.1% | 90 of 90 |
| Arrendamento | 23.2 | 0.7 | 3.1% | — |

Three segments carry the analysis; the others are shown for context.

**The empty field is not describing the borrower. It is describing the lender's
underwriting method.** A bank underwrites against declared revenue, which is why
that field is populated. A fintech underwriting against transaction flow — card
receivables, instant payments, invoice history — has no reason to capture revenue
at all. The missing value is a fingerprint of how the credit decision was made.

That reframing turns a data-quality nuisance into a readable signal: this series
measures how much business credit is granted **without looking at revenue**, and
how fast that practice is spreading.

### Read the table twice

The first reading is the rate: at 40.3%, the fintech segment sits at thirteen
times the bank rate.

The second reading contradicts the headline, and belongs here rather than buried.
**In absolute value, banks hold by far the most credit with no size on file —
R$ 67.8 bn against the fintech segment's R$ 1.4 bn.** Fintechs hold 0.05% of
national business credit. Anyone sizing a market from the fintech line alone would
be sizing something very small.

This project is about the *rate and its trajectory*, not the volume. The rate is
what tells you whether a field can be trusted; the volume tells you how much money
is behind it. They answer different questions, and conflating them is the error
this repository exists to make visible.

---

## Why this matters to anyone working with the data

**If you consume SCR.data**, any analysis that filters or groups by borrower size
silently drops a growing share of fintech lending. The bias is not random: it is
concentrated in the fastest-growing segment. This repository documents where the
field can be trusted and where it cannot.

**If you hold a credit portfolio of your own**, the method transfers. The question
"which fields in my registry degrade, for which counterparties, and from when" is
answerable with the same approach: a control group that barely moves, a stability
criterion that survives its own parameters, and an explicit statement of what the
data cannot answer.

---

## Method

The analysis is deliberately conservative, and the conservatism is declared rather
than assumed.

**Nationwide, 90 months.** The series began as a single state (Paraná) and was
widened when the fintech denominator there proved too small to carry a proportion —
0.07% of credit in the state. The state-level reading turned out to be
representative and conservative, but that was established by running the national
series, not by assuming it.

**Measured in outstanding value, not contract counts.** Counting rows treats a
ten-thousand and a ten-million contract as equal. The contract count is also
withheld for confidentiality in 37.2% of rows, and what is missing is not random —
it concentrates in small cells.

**Suppressed cells are bounded, not dropped.** Where the contract count is withheld,
the cell is counted as holding at least one contract. Dropping those rows would
understate totals *more* in small segments — precisely the ones under study — which
would have biased the filter against fintechs for the wrong reason. Every count
here is therefore a floor and every displacement figure a ceiling: the finding is
stated against itself.

**A control group that moves, but an order of magnitude less.** Banks hold 76.7% of
national business credit. Their unavailable-size share is not flat — it ran at
14.7% in December 2019, fell below 2% through 2020–21, and has climbed back to
3.1%. What matters is the comparison: across the July 2025 cut-off, the `Banco`
line moves 0.32 pp while `Fintech` moves 8.52 pp. A shared shock that hit every
lender would not produce that ratio.

**A stability criterion that applies to everyone — and replaced a worse one.** The
first cut-off was a 1% market-share floor. It was discarded before production: it
excluded segments for being *small* rather than *unstable*, and `Fintech` holds
0.05% of business credit while being the entire subject of the analysis. The rule
now admits a segment-month only where a single contract cannot shift the proportion
by more than 0.1 percentage points. Applied identically to every segment: it keeps
all 90 bank months, 71 fintech months, and 64 payment-institution months.

**The threshold is reported with its sensitivity, not as a single number.** The
finding survives every ceiling tested:

| Ceiling | Months kept | Series starts | First % | Last % | Slope, pp/year |
|---|---:|---|---:|---:|---:|
| 0.05 pp | 69 | 2020-10 | 0.0 | 40.3 | 8.90 |
| 0.10 pp *(used)* | 71 | 2020-08 | 5.0 | 40.3 | 8.52 |
| 0.25 pp | 79 | 2019-12 | 0.1 | 40.3 | 7.55 |
| 0.50 pp | 80 | 2019-11 | 0.0 | 40.3 | 7.45 |
| 1.00 pp | 84 | 2019-07 | 0.0 | 40.3 | 7.05 |
| no filter | 84 | 2019-07 | 0.0 | 40.3 | 7.05 |

Tightening the threshold costs months and *steepens* the slope. There is no
setting at which the rise disappears, which is the only reason to trust any of
them.

---

## What was ruled out

**The source-methodology migration does not explain the finding.** SCR.data is
documented across two methodology versions, and if the fintech rise aligned with
that migration, this would be a collection artefact rather than market behaviour.
It was treated as a veto condition. Three independent lines closed it:

1. **No file from the earlier vintage is in the dataset.** `ingest.py` fetches the
   annual archives from the current endpoint for every year 2019–2026 in a single
   run. All 90 months were served by the publication pipeline as it stands today.
   There is no seam between two vintages, because only one was ever downloaded.
2. **No structural break in the volumes.** At the two dates under suspicion, rows
   read move by +5.1% (March 2019) and −4.6% (July 2025), while rows retained move
   by +1.1% and −1.0%. That is ordinary month-to-month variation. A change in
   collection scope would not be invisible at this level.
3. **The one dated rule in the current methodology does not touch these fields.**
   From January 2025, only operations flagged by the institution as problem assets
   are counted. That governs `ativo_problematico`. This analysis measures `porte`
   and `carteira_ativa`.

Worth stating plainly, because it was the tempting shortcut: the methodology
document contains no changelog and no reprocessing clause. The reassurance had to
come from the data, not from the documentation.

**The December 2023 peak in the bank line is seasonal.** Outstanding grew 3.4% that
month while credit with no size on file grew 30.1% — a numerator effect, not a
shrinking denominator. It is spread across the book rather than concentrated in one
product, and December exceeds November in six of the seven years in the series —
2020 is the exception, and by 0.07 pp. It is year-end reporting behaviour, not a
break.

---

## What this project does not claim

**The segments under study are small.** `Fintech` is 0.05% of national business
credit and `Instituição de pagamento` 0.03%. Small denominators are exactly why the
stability filter exists, and the filter is why 19 fintech months and 26
payment-institution months are excluded rather than plotted. It does not make the
segments large.

**The stability criterion is denominated in contracts while the series is
denominated in value.** The mismatch is deliberate — contracts are the right unit
for asking whether a proportion is stable — but it bites hardest where value
concentrates in few large contracts, which is the payment-institution case. A
value-denominated criterion is the planned fix.

**Unexplained movement in July 2025 on the bank line.** The evidence above
establishes that file composition did not change that month. The bank line moves
0.32 pp across the cut, an order of magnitude below the fintech move, but it is
movement in what should be an inert control and it is not explained.

**A June 2024 discontinuity in fintech contract counts.** Located independently by
the stability diagnosis. The volume checks above were run on whole files, not on
fintech cells, so they do not speak to this. Open.

**No causal claim about underwriting.** The link from an empty field to
transaction-based underwriting is an interpretation consistent with the pattern and
with domain knowledge of how these lenders operate. SCR.data does not record
underwriting method, and nothing here tests it.

**Nothing here identifies a company or a lender.** The registry is aggregated and
cell-suppressed by design, and no attempt is made to work around that.

---

## Segment glossary

The eight segments are groupings the Central Bank builds from each institution's
registered licence type. The mapping below is transcribed from the SCR.data
methodology, not paraphrased from general knowledge:

| Segmento | Licence types (as registered) | What these institutions do |
|---|---|---|
| `Banco` | Banco Múltiplo, Banco Comercial, Banco de Investimento, Banco de Câmbio, Banco Múltiplo Cooperativo, Banco Comercial Estrangeiro; Banco do Brasil and Caixa Econômica Federal are named individually | Full-licence banks, including the two federally controlled ones |
| `Cooperativa` | Cooperativa de Crédito | Credit unions |
| `Desenvolvimento/Fomento` | BNDES, Banco de Desenvolvimento, Agência de Fomento | The national development bank and the state-level development banks and agencies; they lend on policy mandates rather than on commercial underwriting |
| `Financeira` | Sociedade de Crédito, Financiamento e Investimento (SCFI) | Consumer finance companies; no deposit-taking |
| `Arrendamento` | Sociedade de Arrendamento Mercantil | Leasing companies |
| `Fintech` | Sociedade de Crédito Direto (SCD), Sociedade de Empréstimo entre Pessoas (SEP) | Digital-only credit licences created in 2018: an SCD lends its own capital, an SEP matches lenders to borrowers |
| `Instituição de pagamento` | Instituição de Pagamento | Payment institutions authorised to extend credit |
| `Outros` | Associação de Poupança e Empréstimo, Companhia Hipotecária, Sociedade de Crédito ao Microempreendedor, Sociedade Corretora e Distribuidora de TVM | Savings and loan associations, mortgage companies, microcredit companies, and securities brokers and dealers |

Licence names are left in Portuguese for the same reason the segment values are:
they are what the institution is registered as, not a description of it. The third
column carries the meaning.

Two of these matter for reading the finding.

`Fintech` is a regulatory category, not a marketing label — the two licences come
from CMN Resolution 4.656/2018. A digital bank holding a banking licence is **not**
in this segment; it reports as `Banco`. So the segment is much narrower than what
the press calls a fintech, which is part of why it is small.

`Desenvolvimento/Fomento` is dominated by BNDES, the national development bank. It
is the second-largest segment by outstanding credit and it lends on policy
mandates rather than on commercial underwriting, which is worth knowing before
comparing its 6.4% against a commercial lender's.

---

## What is in this repository

```
notebooks/01_unavailable_size.ipynb   analysis, end to end
src/style.py                          chart styling (Synthwave Horizon palette)
src/ingest.py                         month-by-month ingestion from SCR.data
DECISIONS.md                          decision log — including rejected hypotheses
pyproject.toml                        project metadata and direct dependencies
requirements.txt                      the same dependencies, pinned
```

**`DECISIONS.md` is worth reading alongside the analysis.** Every methodological
decision is recorded with its reasoning and — the part that matters — the condition
that would reverse it. It includes the project's original hypothesis, which was
tested and did not survive, and two cut-off criteria, one of which was discarded
before it reached production.

---

## Reproducing

```bash
uv venv --python 3.11
.venv/Scripts/activate        # Windows;  source .venv/bin/activate on Unix
uv pip install -r requirements.txt
uv pip install -e .           # puts src/ on the path — `import style` needs it
```

Raw SCR.data files are not versioned. `ingest.py` downloads and aggregates them;
the ingestion log in `data/processed/` records exactly which monthly files were
consumed — which is also what makes the vintage argument above checkable rather
than asserted.

---

## Data

SCR.data, Central Bank of Brazil, released under ODbL. The registry aggregates
credit operations reported by supervised institutions, with cell-level suppression
where counts are small enough to risk identification.

---

*Built by Marco Sitta — twenty years in Brazilian banking, currently managing
small-business relationships at Banco do Brasil, now working in data.
The domain knowledge is the reason the empty field looked like a signal rather than
a defect.*