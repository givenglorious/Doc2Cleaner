# Doc2Cleaner

A lightweight Python library for cleaning messy scraped data (from Twitter/X, Instagram, or any raw dataset) and turning it into a tidy, structured spreadsheet ready for further analysis.

## Why this library exists

Data collected through web scraping is almost never clean. It's usually full of URLs, mentions, hashtags, emojis, symbols, extra whitespace, and repeated characters (`ayoooo`, `bagusss`), scattered across dozens of inconsistent columns depending on the source.

**textcleaner** was built to remove that friction. Instead of rewriting the same regex cleaning logic for every new scraping project, this library gives you:

- A consistent, reusable way to **load** raw `.xlsx`/`.csv` files
- A simple way to **inspect and drop unnecessary columns** (scraped data often has 10+ irrelevant fields like `user_id`, `retweet_count`, `profile_url`, etc.)
- A **text cleaning pipeline** that strips out noise (links, mentions, hashtags, emojis, numbers, symbols, repeated letters) so the text is ready for downstream NLP work
- A single **orchestration class** (`CleaningPipeline`) that ties everything together and exports a clean spreadsheet

This is especially useful as a preprocessing step for **sentiment analysis, text classification, topic modeling**, or any NLP project where the model needs clean, normalized text rather than raw social media noise.

## Installation

```bash
unzip textcleaner.zip -d textcleaner
cd textcleaner
pip install -e .
```

This installs the package in editable mode, along with its dependencies (`pandas`, `openpyxl`).

## Project structure

```
textcleaner/
├── pyproject.toml
├── cli.py                     # interactive command-line usage
└── textcleaner/
    ├── __init__.py             # public exports
    ├── loader.py                 # DocumentLoader — loads .xlsx / .csv into a DataFrame
    ├── columns.py                  # ColumnCleaner — inspect / drop columns
    ├── cleaner.py                    # TextCleaner — regex-based text cleaning
    └── pipeline.py                    # CleaningPipeline — orchestrates the whole flow
```

## Quick start

```python
from textcleaner import CleaningPipeline

# 1. Load your scraped file
pipeline = CleaningPipeline("YOUR_FILE")

# 2. See what columns are available, and which ones look like text
pipeline.preview_columns()
# Kolom tersedia   : ['username', 'tweet', 'user_id', 'retweet_count', 'created_at']
# Kandidat teks    : ['username', 'tweet']

# 3. Run the cleaning pipeline
result = pipeline.run(
    text_columns=["target"],              # columns whose text should be cleaned
    drop_columns=["columns_1", "columns_2"],  # columns you don't need
    output_path="cleaned.xlsx",          # where to save the result
)

print(result.head())
```

This produces a new file `cleaned.xlsx` with:
- The unnecessary columns removed
- A new `tweet_cleaned` column containing the cleaned text (the original `tweet` column is preserved unless you set `overwrite_original=True`)

## Command-line usage

If you don't want to write a script, use the interactive CLI:

```bash
python cli.py data.xlsx
```

It will:
1. Show you the available columns and suggest which ones look like text
2. Ask which columns to clean
3. Ask which columns to drop
4. Ask for an output filename
5. Save the cleaned file

## What gets cleaned

`TextCleaner` applies the following steps, in order, to every text value:

| Step | What it does | Example |
|---|---|---|
| URLs | Removes `http(s)://...` links | `cek https://x.com` → `cek` |
| pic.twitter.com links | Removes Twitter media links | `pic.twitter.com/xyz` → removed |
| Mentions | Removes `@username` | `@admin halo` → `halo` |
| Hashtags | Removes `#tagname` | `#trending banget` → `banget` |
| Non-ASCII / emoji | Removes emojis and non-ASCII characters | `keren 🔥🔥` → `keren` |
| Symbols | Removes punctuation and special characters | `wow!!!` → `wow` |
| Numbers | Removes digits | `top10` → `top` |
| Repeated characters | Collapses 3+ repeated letters into one | `ayoooo` → `ayo` |
| Newlines | Converts `\n` into a space | |
| Extra whitespace | Collapses multiple spaces into one | |
| Lowercasing | Converts everything to lowercase | |

## Using individual components

Each class can also be used on its own if you only need part of the pipeline.

**Just load a file:**
```python
from textcleaner import DocumentLoader

df = DocumentLoader("data.xlsx").load()
```

**Just clean a single string:**
```python
from textcleaner import TextCleaner

TextCleaner.clean("Ayooooo cek https://link.com @admin 🔥")
# -> "ayo cek"
```

**Just manage columns:**
```python
from textcleaner import ColumnCleaner

cc = ColumnCleaner(df)
cc.suggest_text_columns()          # guess which columns are text
df = cc.drop_columns(["user_id"])  # drop unwanted columns
```

## `CleaningPipeline.run()` options

| Parameter | Type | Description |
|---|---|---|
| `text_columns` | `list[str]` | Columns whose text will be cleaned (required) |
| `drop_columns` | `list[str]` | Columns to remove before cleaning (optional) |
| `output_path` | `str` | Output file path — supports `.xlsx` or `.csv` (default: `"cleaned.xlsx"`) |
| `overwrite_original` | `bool` | If `True`, overwrites the original column instead of creating a `<column>_cleaned` copy (default: `False`) |
| `save` | `bool` | If `True`, automatically saves the result to `output_path` (default: `True`) |

## What this library is NOT for

- It doesn't do language-aware normalization (e.g. turning slang like `gk`, `ga`, `nggak` into `tidak`) — that requires a dictionary-based or NLP approach on top of this
- It doesn't do sentiment analysis, tokenization, or stemming itself — it's meant as the **preprocessing step before** those tasks
- It's not built for LLM-based cleaning — the regex approach here is fast and free for structural noise; LLMs are better reserved for meaning-level tasks like slang normalization or classification

## Roadmap ideas

- Indonesian slang-word normalization via dictionary lookup
- Optional stopword removal (e.g. via Sastrawi for Bahasa Indonesia)
- Optional stemming
- Batch processing for multiple files at once
