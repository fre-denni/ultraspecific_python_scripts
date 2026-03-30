#!/usr/bin/env python3
"""
csv_to_md.py
Scarica un CSV da Google Sheets (o qualsiasi URL pubblico) e trasforma
una colonna specifica in file .md separati.

Uso:
    python csv_to_md.py <url_csv> <cartella_output> \
        --content-col "NomeColonnaContenuto" \
        --title-prefix  "NomeColonnaTitolo"

Esempio:
    python csv_to_md.py \
        "https://docs.google.com/spreadsheets/d/.../export?format=csv" \
        ./output \
        --content-col "Descrizione" \
        --title-prefix "Titolo"
"""

import argparse
import csv
import io
import os
import re
import sys
import urllib.request


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(text: str, max_len: int = 60) -> str:
    """Converte una stringa in un nome file sicuro e leggibile."""
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)   # rimuove caratteri speciali
    text = re.sub(r"[\s_]+", "-", text)                        # spazi → trattini
    text = re.sub(r"-{2,}", "-", text)                         # trattini multipli → uno
    return text[:max_len].strip("-")


def download_csv(url: str) -> list[dict]:
    """Scarica il CSV dall'URL e restituisce una lista di dizionari (una riga = un dict)."""
    print(f"Download CSV da:\n    {url}\n")
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            raw = response.read().decode("utf-8")
    except Exception as e:
        sys.exit(f"X -- Errore durante il download: {e}")

    reader = csv.DictReader(io.StringIO(raw))
    rows = list(reader)
    print(f"   Righe trovate: {len(rows)}")
    print(f"    Colonne disponibili: {list(rows[0].keys()) if rows else '—'}\n")
    return rows


def validate_columns(rows: list[dict], content_col: str) -> None:
    """Verifica che le colonne richieste esistano nel CSV."""
    if not rows:
        sys.exit("X --  Il CSV è vuoto.")
    headers = list(rows[0].keys())
    missing = [c for c in [content_col] if c not in headers]
    if missing:
        sys.exit(
            f"X -- Colonne non trovate: {missing}\n"
            f"    Colonne disponibili: {headers}"
        )


def write_md_files(
    rows: list[dict],
    content_col: str,
    title_prefix: str,
    output_dir: str,
) -> None:
    """Crea un file .md per ogni riga."""
    os.makedirs(output_dir, exist_ok=True)
    total = len(rows)
    pad = len(str(total))          # padding dinamico: 3 cifre per ≤999, 4 per ≤9999, ecc.
    skipped = 0
    created = 0

    for i, row in enumerate(rows, start=1):
        content = row[content_col].strip()
        title   = f"{title_prefix}-{i}"

        # Salta righe senza contenuto
        if not content:
            print(f"  !  Riga {i:>{pad}} — contenuto vuoto, skippata.")
            skipped += 1
            continue

        # Nome file: 001-title_prefix.md
        index   = str(i).zfill(pad)
        filename = f"{index}-{slugify(title_prefix)}.md"        
        filepath = os.path.join(output_dir, filename)

        # Scrivi il file
        with open(filepath, "w", encoding="utf-8") as f:
            # Intestazione Markdown opzionale
            f.write(content)
            f.write("\n")

        created += 1

        # Progresso ogni 50 file (o sempre se totale < 50)
        if total <= 50 or i % 50 == 0 or i == total:
            pct = i / total * 100
            print(f"  [{i:>{pad}}/{total}] {pct:5.1f}%  →  {filename}")

    print(f"\n  Fatto!  Creati: {created}  |  Saltati: {skipped}")
    print(f"    Cartella output: {os.path.abspath(output_dir)}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Converte una colonna CSV in file .md separati.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("url",        help="URL del file CSV (es. Google Sheets export link)")
    parser.add_argument("output_dir", help="Cartella di destinazione dei file .md")
    parser.add_argument(
        "--content-col", required=True,
        metavar="COLONNA",
        help="Nome esatto della colonna da usare come contenuto del file .md"
    )
    parser.add_argument(
        "--title-prefix",
        required=True,
        metavar="PREFISSO",
        help="Prefisso per dare titolo ai file.md"
    )

    args = parser.parse_args()

    rows = download_csv(args.url)
    validate_columns(rows, args.content_col)
    write_md_files(rows, args.content_col, args.title_prefix, args.output_dir)


if __name__ == "__main__":
    main()