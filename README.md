<p align="center">
  <img src="assets/banner.png" alt="doc2cleaner" width="100%" />
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2ea44f" alt="License: MIT"></a>
  <a href="https://github.com/givenglorious/doc2cleaner/releases"><img src="https://img.shields.io/github/v/release/givenglorious/doc2cleaner?label=version&color=1f6feb" alt="Version"></a>
  <img src="https://img.shields.io/badge/python-3.9%2B-blue" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/pandas-2.0%2B-150458" alt="Pandas">
</p>

# doc2cleaner

> **Stop rewriting the same cleaning logic. Start cleaning.**
>
> A lightweight Python library for cleaning messy scraped data — from Twitter/X, Instagram, or any raw dataset — and turning it into a tidy, structured spreadsheet ready for NLP analysis.

---

## Why this exists

Scraped data is never clean. URLs, mentions, hashtags, emojis, repeated characters (`ayoooo`, `bagusss`), and dozens of irrelevant columns — all before you've even started the actual analysis.

`doc2cleaner` removes that friction with a consistent, reusable pipeline so you spend less time on preprocessing and more time on the work that matters.

---

## What it does

- **Loads** raw `.xlsx` and `.csv` files into a clean DataFrame
- **Inspects and drops** unnecessary columns (scraped data often has 10+ irrelevant fields)
- **Cleans text** — strips URLs, mentions, hashtags, emojis, symbols, numbers, and repeated characters
- **Exports** a clean spreadsheet ready for sentiment analysis, classification, or topic modeling
- **CLI support** — run the full pipeline interactively without writing a script

---

## Installation

```bash
unzip doc2cleaner.zip -d doc2cleaner
cd doc2cleaner
pip install -e .
```

Installs in editable mode with dependencies: `pandas`, `openpyxl`.

---

## Quick Start

```python
from textcleaner import CleaningPipeline

pipeline = CleaningPipeline("data.xlsx")
pipeline.preview_columns()

result = pipeline.run(
    text_columns=["tweet"],
    drop_columns=["user_id", "retweet_count"],
    output_path="cleaned.xlsx",
)
```

Output: a new `cleaned.xlsx` with unnecessary columns removed and a `tweet_cleaned` column containing normalized text.

---

## CLI Usage

```bash
python cli.py data.xlsx
```

The CLI walks you through column selection, cleaning options, and output filename interactively — no script needed.

---

## Cleaning Pipeline

Every text value goes through these steps, in order:

| Step | What it removes | Example |
|---|---|---|
| URLs | `http(s)://...` links | `cek https://x.com` → `cek` |
| Twitter media | `pic.twitter.com/...` links | removed entirely |
| Mentions | `@username` | `@admin halo` → `halo` |
| Hashtags | `#tagname` | `#trending banget` → `banget` |
| Emoji / non-ASCII | Emojis and non-ASCII characters | `keren 🔥` → `keren` |
| Symbols | Punctuation and special characters | `wow!!!` → `wow` |
| Numbers | Digits | `top10` → `top` |
| Repeated chars | 3+ repeated letters collapsed | `ayoooo` → `ayo` |
| Whitespace | Newlines and extra spaces normalized | |
| Lowercase | Full lowercasing | `MANTAP` → `mantap` |

---

## Individual Components

Each class works standalone if you only need part of the pipeline.

```python
# Load a file
from textcleaner import DocumentLoader
df = DocumentLoader("data.xlsx").load()

# Clean a single string
from textcleaner import TextCleaner
TextCleaner.clean("Ayooooo cek https://link.com @admin 🔥")
# → "ayo cek"

# Manage columns
from textcleaner import ColumnCleaner
cc = ColumnCleaner(df)
cc.suggest_text_columns()
df = cc.drop_columns(["user_id"])
```

---

## `CleaningPipeline.run()` Options

| Parameter | Type | Default | Description |
|---|---|---|---|
| `text_columns` | `list[str]` | required | Columns to clean |
| `drop_columns` | `list[str]` | `[]` | Columns to remove before cleaning |
| `output_path` | `str` | `"cleaned.xlsx"` | Output path — `.xlsx` or `.csv` |
| `overwrite_original` | `bool` | `False` | Overwrite original column instead of creating `_cleaned` copy |
| `save` | `bool` | `True` | Auto-save result to `output_path` |

---

## Project Structure

```
doc2cleaner/
├── pyproject.toml
├── cli.py                  ← Interactive CLI
└── textcleaner/
    ├── __init__.py         ← Public exports
    ├── loader.py           ← DocumentLoader
    ├── columns.py          ← ColumnCleaner
    ├── cleaner.py          ← TextCleaner
    └── pipeline.py         ← CleaningPipeline
```

---

## What This Is Not

- **Not a slang normalizer** — converting `gk`, `ga`, `nggak` → `tidak` requires a dictionary-based approach on top of this
- **Not an NLP engine** — no sentiment analysis, tokenization, or stemming; this is the preprocessing step *before* those tasks
- **Not LLM-based** — regex is fast and free for structural noise; LLMs are better reserved for meaning-level tasks

---

## Roadmap

- Indonesian slang normalization via dictionary lookup
- Optional stopword removal (Sastrawi support)
- Optional stemming
- Batch processing for multiple files

---

## License

MIT: [LICENSE](LICENSE)

---

<p align="center"><em>"Clean data in. Better models out."</em></p>
