# Archive

Superseded work, kept rather than deleted. The decision log's rule applies here
too: a revised entry is amended and pointed forward, never erased. The trail is
the asset.

## `01_credito_sem_faturamento.ipynb`

The first complete version of this analysis. Thirty cells, written in Portuguese
and written to be *read* — the reasoning is spelled out at length in prose rather
than compressed into comments. It carries its original outputs.

**Scope:** business credit in the state of Paraná, January 2019 to May 2026.
**Superseded by:** `notebooks/01_unavailable_size.ipynb` (nationwide, English).

### Why it was superseded

Fintechs hold roughly 0.07% of credit in Paraná. At that size the denominator is
too small for the finding to be defensible: a handful of contracts moves the
proportion, and no amount of careful writing fixes that. Widening to the whole
country multiplied the denominator about fifteenfold. The headline figures moved
with it — 1% / 11% / 31% for banks, payment institutions and fintechs in Paraná
became 3.1% / 8.0% / 40.3% nationwide.

### Why it is still here

**It is the evidence for an amendment.** This notebook reads the bank line as
flat at around 2% for seven years and calls it close to a perfect control group.
Nationwide that is false — the line runs from roughly 1.4% to 14.7%. The error
was not carelessness; it is what the Paraná data actually looks like. Keeping the
outputs keeps the proof that a line can look immobile at one scale and move by a
factor of ten at another. Deleting the file would leave the amendment in
`DECISIONS.md` asserting something no longer checkable.

**Its section 8 was recovered, not replaced.** The sensitivity analysis —
recomputing the whole conclusion under several ceilings, including no filter at
all — was written here first and had been dropped in the rewrite. It now lives in
section 5.1 of the current notebook, run nationwide. Two other passages came back
the same way: the argument against a market-share floor, and the caveat that the
stability metric is a floor on displacement rather than a measurement of it.

That is the practical reason this folder exists. The rewrite lost material worth
keeping, and nobody noticed until the old file was read again.

### What not to do with it

Do not cite its figures. They are Paraná and they are superseded. Read it for the
reasoning, and for what the same question looked like before the scope changed.
