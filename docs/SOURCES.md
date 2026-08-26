# Source documents

The two PDFs in this folder are the Central Bank of Brazil's own methodology
notes for SCR.data. They are committed rather than linked because section 6 of
`notebooks/01_unavailable_size.ipynb` rests an argument on them: a conclusion
whose evidence does not travel with the repository cannot be audited.

Both are public documents published by the Banco Central do Brasil under the
dataset's Open Data Commons Open Database License (ODbL).

## What is here

| File | Covers | Downloaded | Size | MD5 |
|---|---|---|---|---|
| `scr_data_metodologia.pdf` | SCR.data version 1 | 2026-08-17 | 550,671 B | `686ba909acce37e4436855857860460e` |
| `metodologia_versao2.pdf` | SCR.data version 2 | 2026-08-17 | 356,060 B | `a9e9f918084096f41739ba8285a01a76` |

Source pages, both reachable from the dataset landing page at
<https://dadosabertos.bcb.gov.br/dataset/scr_data>:

- <https://www.bcb.gov.br/content/estabilidadefinanceira/scr/scr.data/scr_data_metodologia.pdf>
- <https://www.bcb.gov.br/pda/desig/metodologia_versao2.pdf>

## Why the hashes are recorded

The Central Bank revises published artefacts in place, without renaming them or
announcing it. This is not speculation about the PDFs — it is documented
behaviour of the same publisher for the same dataset: `src/ingest.py` compares
`Content-Length` against the local copy on every run precisely because of it, and
that check caught the 2024 and 2025 monthly archives being revised at source
after they had already been downloaded and analysed.

A reader who finds a different file at the URLs above can compare the hash and
know immediately whether they are reading the document this analysis read. The
argument in section 6 depends on what these specific files say.

## What is not here

`tutorial.pdf` (<https://www.bcb.gov.br/content/estabilidadefinanceira/scr/scr.data/tutorial.pdf>)
explains how to download and open the dataset. Nothing in the analysis rests on
it, so it stays out of the repository.

## One thing the dataset page settles

Versions 1 and 2 are published as **separate downloads**, not as one series that
switched format partway through. `src/ingest.py` fetches only the version 2
archives, from `https://www.bcb.gov.br/pda/desig/scrdata_{year}.zip`. So the
extract analysed here cannot contain a mix of the two, which closes off one shape
the version objection in section 6 could otherwise have taken.
