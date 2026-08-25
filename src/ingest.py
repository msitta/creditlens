'''
SCR.data (BACEN) — Version 2 ingestion pipeline.

Downloads the yearly ZIP archives published by the Banco Central do Brasil,
reads the monthly CSVs straight from inside the archives, filters to a single
client type and state, and writes one consolidated Parquet file.

Source : https://dadosabertos.bcb.gov.br/dataset/scr_data
License: Open Data Commons Open Database License (ODbL)

Four format traps handled here, all confirmed by profiling the raw files:

  1. UTF-8 BOM on the header line. Without encoding='utf-8-sig' the first
     column is silently named '\ufeffdata_base' and every lookup on it fails.
  2. Field separator is ';' AND at least one category value contains ';'
     inside it ('Comercio; reparacao de veiculos automotores e motocicletas').
     Quoting must be respected or the row shifts by one column.
  3. Decimal separator is ',' on every monetary column.
  4. numero_de_operacoes = -1 is a DISCLOSURE SUPPRESSION FLAG, not a count.
     It appears in roughly a quarter of all rows. Left as -1 it destroys any
     mean, sum or ratio built on that column. Here it becomes NA plus an
     explicit boolean flag so the suppression itself stays analysable.
'''

import io
import json
import zipfile
from pathlib import Path

import pandas as pd
import requests

# --- configuration -------------------------------------------------------

YEARS = range(2019, 2027)
UF_KEEP = None          # None = nationwide; 'PR' restores the original state cut
CLIENT_KEEP = 'PJ'

BASE_URL = 'https://www.bcb.gov.br/pda/desig/scrdata_{year}.zip'
RAW_DIR = Path('data/raw')
OUT_DIR = Path('data/processed')
CHUNK_ROWS = 200_000

MONEY_COLS = [
    'a_vencer_ate_90_dias',
    'a_vencer_de_91_ate_360_dias',
    'a_vencer_de_361_ate_1080_dias',
    'a_vencer_de_1081_ate_1800_dias',
    'a_vencer_de_1801_ate_5400_dias',
    'a_vencer_acima_de_5400_dias',
    'carteira_a_vencer',
    'vencido_de_15_ate_90_dias',
    'vencido_acima_de_90_dias',
    'carteira_vencida',
    'carteira_ativa',
    'carteira_inadimplencia',
    'ativo_problematico',
]

CATEGORY_COLS = [
    'uf',
    'segmento',
    'cliente',
    'cnae_ocupacao',
    'porte',
    'modalidade',
    'submodalidade',
    'origem',
    'indexador',
]

SUPPRESSION_SENTINEL = -1

# --- download ------------------------------------------------------------


def download_year(year, raw_dir=RAW_DIR):
    '''Fetch one yearly archive, skipping the download if it is already local.'''
    raw_dir.mkdir(parents=True, exist_ok=True)
    target = raw_dir / f'scrdata_{year}.zip'

    if target.exists() and target.stat().st_size > 0:
        print(f'[skip]     {target.name} already present '
              f'({target.stat().st_size / 1e6:.0f} MB)')
        return target

    url = BASE_URL.format(year=year)
    print(f'[download] {url}')
    with requests.get(url, stream=True, timeout=600) as response:
        response.raise_for_status()
        with open(target, 'wb') as handle:
            for block in response.iter_content(chunk_size=1 << 20):
                handle.write(block)

    print(f'[ok]       {target.name} ({target.stat().st_size / 1e6:.0f} MB)')
    return target


# --- read ----------------------------------------------------------------


def read_member(archive, member, uf_keep=UF_KEEP, client_keep=CLIENT_KEEP):
    '''Read one monthly CSV from inside the archive, filtering as we go.

    Filtering happens chunk by chunk so peak memory stays flat regardless of
    how many years are being ingested. A full monthly file is ~100 MB and
    ~315k rows; the PJ/PR slice is under 9k rows.
    '''
    kept = []
    rows_seen = 0

    with archive.open(member) as raw:
        buffer = io.TextIOWrapper(raw, encoding='utf-8-sig')
        reader = pd.read_csv(
            buffer,
            sep=';',
            quotechar='"',
            dtype=str,  # decimal=',' would be ignored here; see coerce_types
            chunksize=CHUNK_ROWS,
        )
        for chunk in reader:
            rows_seen += len(chunk)
            mask = pd.Series(True, index=chunk.index)
            if uf_keep:
                mask &= chunk['uf'] == uf_keep
            if client_keep:
                mask &= chunk['cliente'] == client_keep
            if mask.any():
                kept.append(chunk.loc[mask])

    frame = (pd.concat(kept, ignore_index=True) if kept
             else pd.DataFrame(columns=[]))
    return frame, rows_seen


# --- clean ---------------------------------------------------------------


def coerce_types(frame):
    '''Cast the raw string columns into real types.

    Everything is read as str first so that pandas never guesses a dtype from
    a partial chunk and then contradicts itself on the next one.
    '''
    frame = frame.copy()

    frame['data_base'] = pd.to_datetime(frame['data_base'], errors='coerce')

    # Profiling confirmed BACEN publishes no thousands separator (values look
    # like '11151215110,12'). The '.' strip is defensive: if that ever changes,
    # this still parses; as it stands it is a no-op.
    for column in MONEY_COLS:
        frame[column] = pd.to_numeric(
            frame[column].str.replace('.', '', regex=False)
                         .str.replace(',', '.', regex=False),
            errors='coerce',
        )

    operations = pd.to_numeric(frame['numero_de_operacoes'], errors='coerce')

    # Trap 4: -1 means "withheld for disclosure control", not "minus one".
    frame['operacoes_suprimidas'] = operations.eq(SUPPRESSION_SENTINEL)
    frame['numero_de_operacoes'] = operations.mask(
        operations.eq(SUPPRESSION_SENTINEL))

    for column in CATEGORY_COLS:
        frame[column] = frame[column].astype('category')

    # Porte is derived from declared gross revenue in the client's
    # registration record. 'Indisponivel' therefore means the revenue field
    # is missing upstream — this flag is the subject of the analysis, so it
    # gets promoted to a first-class column rather than staying buried in a
    # category level.
    frame['porte_indisponivel'] = (
        frame['porte'].astype(str).str.strip().str.lower() == 'indisponível')

    return frame


# --- orchestration -------------------------------------------------------


def ingest(years=YEARS, uf_keep=UF_KEEP, client_keep=CLIENT_KEEP):
    '''Run the whole pipeline and return the consolidated frame plus a log.'''
    frames = []
    log = {
        'uf': uf_keep,
        'cliente': client_keep,
        'months': [],
        'rows_read': 0,
        'rows_kept': 0,
    }

    for year in years:
        path = download_year(year)
        with zipfile.ZipFile(path) as archive:
            members = sorted(
                name for name in archive.namelist()
                if name.lower().endswith('.csv'))
            for member in members:
                frame, rows_seen = read_member(
                    archive, member, uf_keep, client_keep)
                frames.append(coerce_types(frame))
                log['rows_read'] += rows_seen
                log['rows_kept'] += len(frame)
                log['months'].append({
                    'file': member,
                    'rows_read': rows_seen,
                    'rows_kept': len(frame),
                })
                print(f'  {member}: {rows_seen:>7,} read -> '
                      f'{len(frame):>6,} kept')

    combined = pd.concat(frames, ignore_index=True)
    combined = combined.sort_values(['data_base', 'modalidade']) \
                       .reset_index(drop=True)

    log['suppression_rate'] = round(
        float(combined['operacoes_suprimidas'].mean()), 4)
    log['porte_indisponivel_rate'] = round(
        float(combined['porte_indisponivel'].mean()), 4)
    log['date_min'] = str(combined['data_base'].min().date())
    log['date_max'] = str(combined['data_base'].max().date())

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stem = f'scrdata_{client_keep.lower()}_{(uf_keep or "br").lower()}'
    try:
        output = OUT_DIR / f'{stem}.parquet'
        combined.to_parquet(output, index=False)
    except ImportError:
        # No pyarrow/fastparquet available: keep going with a portable format
        # rather than losing the whole run at the last step.
        output = OUT_DIR / f'{stem}.csv.gz'
        combined.to_csv(output, index=False, compression='gzip')
        print('[warn]     no parquet engine found, wrote gzipped CSV instead')
    with open(OUT_DIR / f'{stem}_ingestion_log.json', 'w',
              encoding='utf-8') as handle:
        json.dump(log, handle, ensure_ascii=False, indent=2)

    print(f'\nrows read      : {log["rows_read"]:,}')
    print(f'rows kept      : {log["rows_kept"]:,}')
    print(f'period         : {log["date_min"]} -> {log["date_max"]}')
    print(f'suppressed ops : {log["suppression_rate"]:.1%}')
    print(f'porte missing  : {log["porte_indisponivel_rate"]:.1%}')
    print(f'written        : {output}')

    return combined, log


if __name__ == '__main__':
    ingest()
